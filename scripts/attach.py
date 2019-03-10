# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0703,R0903,R0902
""" Import files into Odoo ir.attachement records
"""


# --------------------------- REQUIRED LIBRARIES ------------------------------


import argparse
import uuid
import odoorpc
import magic
import os
import sys
import locale
import base64
import hashlib
import re
import urllib
import urlparse


# -------------------------------- CONSTANTS ----------------------------------


VM_CONNECTION = u'Connecting server: %s:%s'
VM_CONNECTION_OK = u'Connected'
VM_CONNECTION_FAIL = u'Could not connect'
VM_LOGIN = u'Login with %s@%s'
VM_LOGIN_OK = u'Logged in'
VM_LOGIN_FAIL = u'Could not logged in'
VM_MIME = u'Detecting mime type...'
VM_MIME_MGC = u'Searching for magic file...'
VM_MIME_MIME = u'Searching for mimetype...'
VM_MIME_FOUND = u'File is %s'
VM_MIME_FAIL = u'There was no result from mimemagic'
VM_FILE_READ = u'Reading file'
VM_FILE_READ_OK = u'File has been readed'
VM_FILE_READ_FAIL = u'File could not be readed'
VM_EXIST = u'Looking for a match in the database...'
VM_EXIST_OK = u'Found similar attachment with id %s'
VM_EXIST_FAIL = u'Match not found for resource'
VM_BUILD = u'Building data will be used in the new record...'
VM_BUILD_NAME = u'name        : %s'
VM_BUILD_TYPE = u'type        : %s'
VM_BUILD_PUBLIC = u'public      : %s'
VM_BUILD_MIMETYPE = u'mimetype    : %s'
VM_BUILD_DATAS_FNAME = u'datas_fname : %s'
VM_BUILD_URL = u'url         : %s'
VM_BUILD_DATAS = u'datas       : %s'
VM_WRITE = u'Write new record in database %s'
VM_INSERT_RESULT = u'New record has been created with ID: #%s'
VM_UPDATE_RESULT = u'Existing record has been updated'
VM_WRITE_FAIL = u'New record could not be stored. %s'
WM_WRITE_CANCEL = u'Write proccess is being canceled'
VM_LOGOUT = u'Login out...'
WM_LOGOUT_RESULT = u'Exiting with code %s'
WM_REMOVE = u'Removing related attachment'
WM_REMOVE_OK = u'Related attachment has been deleted'
WM_REMOVE_FAIL = u'Related attachment could not be deleted. {}'
WM_REMOVE_ASSERT = u'There are more than one record related to this file'
WM_REMOVE_CANCEL = u'There is not a record related with to file'


# -------------------------- MAIN SCRIPT BEHAVIOR -----------------------------


class MessageType(object):
    """ Type of message """
    Debug = 0
    Info = 1
    Warn = 2
    Error = 3



class App(object):
    """ Application main controller, this class has been defined following the
    singleton pattern to ensures only one object can be instantiated.
    """

    __instance = None


    def __new__(cls):
        """ Prevent multiple instances from self (Singleton Pattern)
        """

        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            cls.__instance.name = "The one"
        return cls.__instance


    def __init__(self):
        self._input_file = None
        self._title = None
        self._server = None
        self._port = None
        self._database = None
        self._user = None
        self._password = None
        self._cp = locale.getpreferredencoding()
        self._magic_file = None
        self._odoo = None
        self._level = None
        self._overwrite = None
        self._remove = None
        self._markdown = None


    def _argparse(self):
        """ Detines an user-friendly command-line interface and proccess its
        arguments.
        """

        description = u'Import a files into Odoo ir.attachement records'

        parser = argparse.ArgumentParser(description)
        parser.add_argument('file', metavar='file', type=str,
                            help=u'path of the resource file will be stored')

        parser.add_argument('-s', '--server', type=str, dest='server',
                            default=u'localhost',
                            help=u'Odoo server address will be used to connect')

        parser.add_argument('-n', '--port', type=str, dest='port',
                            default=u'8069',
                            help=u'Odoo server port will be used to connect')

        parser.add_argument('-u', '--user', type=str, dest='user',
                            default=u'admin',
                            help=u'user will be used to login in Odoo server')

        parser.add_argument('-p', '--password', type=str, dest='password',
                            default=u'admin',
                            help=u'password will be used to login in Odoo server')

        parser.add_argument('-d', '--database', type=str, dest='database',
                            default=u'odoo_service',
                            help=u'name of the database will be used to store the resource')

        parser.add_argument('-m', '--magic-file', type=str, dest='magic_file',
                            default=u'c:\\Windows\\System32\\magic.mgc',
                            help=u'path to the mime matic mgc file')

        parser.add_argument('-t', '--title', type=str, dest='title',
                            default=unicode(uuid.uuid4()).upper(),
                            help=u'resource title')

        parser.add_argument('-r', '--remove', action='store_true',
                            dest='remove', help='remove related record')

        msg = u'Allow to overwrite existing record or to break when record already exists'
        parser.add_argument('-o', '--overwrite', action='store_true',
                            dest='overwrite', help=msg)

        parser.add_argument('-k', '--file-is-markdown', action='store_true',
                            dest='markdown', help='file argument is a markdown')

        parser.add_argument('-v', '--verbose-level', type=int, dest='verbose_level',
                            default=1, help='verbose level')


        args = parser.parse_args()

        self._input_file = os.path.abspath(args.file.decode(self._cp, errors='replace'))
        self._server = args.server
        self._port = args.port
        self._user = args.user
        self._password = args.password
        self._database = args.database
        self._magic_file = os.path.abspath(args.magic_file.decode(self._cp, errors='replace'))
        self._title = args.title
        self._level = args.verbose_level
        self._overwrite = args.overwrite
        self._remove = args.remove
        self._markdown = args.markdown


    def _proccess(self, path, title):
        """ Performs the conversion from xls to xlsx
        """

        _id = self._already_exists(path)

        if self._remove:
            self._verbose(MessageType.Info, WM_REMOVE)

            if _id:
                try:
                    assert len(_id) == 1, WM_REMOVE_ASSERT
                    model_obj = self._odoo.env['ir.attachment']
                    item = model_obj.browse(_id)
                    item.unlink()
                    self._verbose(MessageType.Debug, WM_REMOVE_OK)
                except Exception as ex:
                    self._verbose(MessageType.Warn, WM_REMOVE_FAIL, ex.message)
            else:
                self._verbose(MessageType.Warn, WM_REMOVE_CANCEL)

        elif len(_id) == 0 or self._overwrite:

            data = self._read_file(path)

            if data:
                mimetype = self._get_mimetype(path)
                _id = self._write_attachment(data, mimetype, path, title, _id)
        else:
            self._verbose(MessageType.Warn, WM_WRITE_CANCEL)
            return 0

        return _id


    def _connect(self):
        """ Connects to a Odoo server """

        result = False

        self._verbose(MessageType.Info, VM_CONNECTION, self._server, self._port)

        try:
            self._odoo = odoorpc.ODOO(self._server, port=self._port)
            result = True
        except Exception as ex:
            self._verbose(MessageType.Warn, VM_CONNECTION_FAIL, ex.message)

        self._verbose(MessageType.Debug, VM_CONNECTION_OK)

        return result


    def _login(self):
        """ Tries to login with user and password or renew session
        """
        result = False

        self._odoo.logout()

        self._odoo.config['timeout'] = 120;

        self._verbose(MessageType.Info, VM_LOGIN, self._server, self._port)

        try:
            self._odoo.login(self._database, self._user, self._password)
            result = True
        except Exception:
            pass

        if not result:
            try:
                self._odoo.login(self._database)
                result = True
            except Exception:
                pass

        if result:
            self._verbose(MessageType.Debug, VM_LOGIN_OK)
        else:
            self._verbose(MessageType.Warn, VM_LOGIN_FAIL)

        return result


    def _verbose(self, message_type, message_name, *arg):
        """ Prints messages """

        try:
            msg = message_name % arg
        except:
            msg= message_name
            print(arg)

        if message_type == MessageType.Debug and self._level <= MessageType.Debug:
            msg = u'  ' + msg
            print(msg)
        elif message_type == MessageType.Warn and self._level <= MessageType.Warn:
            msg = u'  *' + msg
            print(msg)
        elif message_type == MessageType.Error and self._level <= MessageType.Error:
            msg = u'  **' + msg
            print(msg)
        elif  message_type == MessageType.Info and self._level <= MessageType.Info:
            print(msg)


    def _get_mimetype(self, path):
        """ Detect mimetype for file """
        result = None

        self._verbose(MessageType.Info, VM_MIME)
        try:
            self._verbose(MessageType.Debug, VM_MIME_MGC)
            mime = magic.Magic(mime=True, magic_file=self._magic_file)

            self._verbose(MessageType.Debug, VM_MIME_MIME)
            path = path.encode(self._cp)
            result = mime.from_file(path)

            self._verbose(MessageType.Debug, VM_MIME_FOUND, result)
        except Exception:
            self._verbose(MessageType.Warn, VM_MIME_FAIL)
            result = u'application/octet-stream'

        return result


    def _read_file(self, path):
        """ Reads data from file
        """
        data = None

        self._verbose(MessageType.Info, VM_FILE_READ)

        try:
            with open(path, u'rb') as fhandle:
                data = fhandle.read()
                fhandle.close()
            self._verbose(MessageType.Debug, VM_FILE_READ_OK)
        except Exception as ex:
            self._verbose(MessageType.Warn, VM_FILE_READ_FAIL, ex.message)

        return data


    def _already_exists(self, path):
        """ Checks if attachment is already in the database """

        result = False

        model_obj = self._odoo.env['ir.attachment']
        url = self.path_to_url(path)

        self._verbose(MessageType.Info, VM_EXIST)
        result = model_obj.search([('url', '=', url)])

        if result:
            self._verbose(MessageType.Debug, VM_EXIST_OK, result)
        else:
            self._verbose(MessageType.Debug, VM_EXIST_FAIL)

        return result


    def _write_attachment(self, data, mimetype, path, title, _id=False):
        """ Insert new record in ir_attachment table """
        model_obj = self._odoo.env['ir.attachment']

        self._verbose(MessageType.Info, VM_BUILD)
        values = dict(
            name=title,
            type='binary',
            public=False,
            mimetype=mimetype,
            datas_fname=os.path.basename(path),
            url=self.path_to_url(path),
            datas=base64.b64encode(data)
        )

        self._print_values(values, data)

        result = -1
        try:
            self._verbose(MessageType.Info, VM_WRITE, self._database)

            if not _id:
                result = model_obj.create(values)

                if result:
                    self._verbose(MessageType.Debug, VM_INSERT_RESULT, result)
                else:
                    self._verbose(MessageType.Debug, VM_WRITE_FAIL, \
                        u'RPC do not return any valid id')
            else:
                assert len(_id) == 1, u'There are %s record matches' % len(_id)

                item = model_obj.browse(_id)
                answer = item.write(values)

                if answer:
                    self._verbose(MessageType.Debug, VM_UPDATE_RESULT)
                    result = _id
                else:
                    self._verbose(MessageType.Warn, VM_WRITE_FAIL, \
                        u'model write method returns False')

        except Exception as ex:
            self._verbose(MessageType.Warn, VM_WRITE_FAIL, ex.message)

        return result


    def _print_values(self, values, data):
        """ Prints values """
        self._verbose(MessageType.Debug, VM_BUILD_NAME, values['name'])
        self._verbose(MessageType.Debug, VM_BUILD_TYPE, values['type'])
        self._verbose(MessageType.Debug, VM_BUILD_PUBLIC, values['public'])
        self._verbose(MessageType.Debug, VM_BUILD_MIMETYPE, values['mimetype'])
        self._verbose(MessageType.Debug, VM_BUILD_DATAS_FNAME, values['datas_fname'])
        self._verbose(MessageType.Debug, VM_BUILD_URL, values['url'])
        self._verbose(MessageType.Debug, VM_BUILD_DATAS, self._compute_checksum(data))


    def _logout(self):
        """ Loggout from Odoo server """
        self._verbose(MessageType.Info, VM_LOGOUT)
        self._odoo.logout()


    @staticmethod
    def _compute_checksum(bin_data):
        """ compute the checksum for the given datas
            :param bin_data : datas in its binary form
        """
        # an empty file has a checksum too (for caching)
        return hashlib.sha1(bin_data or '').hexdigest()


    def _read_markdown(self):
        """ Reads all image links splitting title and path"""
        attachments = []

        with open(self._input_file) as fhandle:
            for line in fhandle:
                line = u'' + line.decode('utf-8', errors='replace')
                match = re.match(r'^!\[(?P<title>[^]]+)]\((?P<path>[^)]+)\)$', line, re.UNICODE)

                if match:
                    parts = match.groupdict()

                    if parts and len(parts) == 2:
                        parts['path'] = os.path.abspath(parts['path'])
                        attachments.append(parts)

        return attachments

    def _get_attachments(self):
        """ If file is markdown reads it getting links and path else
        input file and title argument will be used instead
        """
        attachments = []

        if self._markdown:
            self._verbose(MessageType.Info, u'Parsing markdown file %s', self._input_file)
            attachments = self._read_markdown()
            self._verbose(MessageType.Debug, u'%s links were found', len(attachments))
        else:
            attachments.append({
                'path': self._input_file,
                'title': self._title
            })

        return attachments

    @staticmethod
    def path_to_url(path):
        """ Transforms a path in a url: file:/// """

        if isinstance(path, unicode):
            path = path.encode('utf8')
        purl = urllib.pathname2url(path)
        return urlparse.urljoin(u'file:', purl)

    def main(self):
        """ The main application behavior, this method should be used to
        start the application.
        """
        result = -1

        # self._argparse()

        # if self._markdown:
        #     self._verbose(MessageType.Info, u'Parsing markdown file %s', self._input_file)
        #     items = self._read_markdown()

        #     self._verbose(MessageType.Debug, u'%s links were found', len(items))
        #     for item in items:
        #         self._verbose(MessageType.Info, u'ITEM %s -> %s', item['title'], item['path'])
        #         result = self._proccess(item['path'], item['title'])
        #         if result < 1:
        #             sys.exit(result)
        #     result = 0
        # else:
        #     result = self._proccess(self._input_file, self._title)

        #     if isinstance(result, list):
        #         result = result[0] if len(result) else 0

        #     self._verbose(MessageType.Info, WM_LOGOUT_RESULT, result)

        self._argparse()

        attachments = self._get_attachments()

        result = -len(attachments)

        if self._connect():

            if self._login():
                for attach in attachments:
                    self._verbose(MessageType.Info, u'Processing %s', attach['title'])
                    self._proccess(attach['path'], attach['title'])

                self._logout()

        sys.exit(result)



# --------------------------- SCRIPT ENTRY POINT ------------------------------

App().main()


