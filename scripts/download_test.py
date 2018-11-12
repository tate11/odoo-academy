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


# -------------------------- MAIN SCRIPT BEHAVIOR -----------------------------


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
        self._server = None
        self._port = None
        self._database = None
        self._user = None
        self._password = None
        self._odoo = None

        self._title = None
        self._id = None
        self._report = None
        self._output = None

        self._cp = locale.getpreferredencoding()


    def _argparse(self):
        """ Detines an user-friendly command-line interface and proccess its
        arguments.
        """

        description = u'Import a files into Odoo ir.attachement records'

        parser = argparse.ArgumentParser(description)
        # parser.add_argument('file', metavar='file', type=str,
        #                     help=u'path of the resource file will be stored')

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

        parser.add_argument('-i', '--id', type=int, dest='id',
                            default=0,
                            help=u'test identifier')

        parser.add_argument('-t', '--tittle', type=str, dest='title',
                            default=None,
                            help=u'test title')

        parser.add_argument('-r', '--report', type=str, dest='report',
                            default=u'academy_tests.view_at_test_qweb',
                            help=u'available test report')

        parser.add_argument('-o', '--output', type=str, dest='output',
                            default=u'Enunciado.pdf',
                            help=u'destination file')


        args = parser.parse_args()

        self._server = args.server
        self._port = args.port
        self._user = args.user
        self._password = args.password
        self._database = args.database
        self._report = args.report
        self._output = os.path.abspath(args.output)


        if args.id > 0:
            self._id = args.id
        elif not self._title:
            files = [item for item in os.listdir(u'.') if item.endswith(u'.ID')]
            if files:
                self._id = int(files[0][:-3])
                self._read_id_file(files[0])
                print u'Using file ' + files[0] + ' and ' + self._report

        if args.title:
            self._title = args.title.decode(self._cp, errors=u'replace')

    def _read_id_file(self, fname):
        """ Read specifications from ID file """
        with open(fname, 'r') as finput: #open the file
            lines = finput.readlines()
            for line_raw in lines:
                line = line_raw.decode('utf-8', errors='replace')
                if re.match(r'^report\= *[^ ]+ *$', line, re.IGNORECASE):
                    self._report = line.replace(u'report=', u'').strip()

    def _connect(self):
        """ Connects to a Odoo server """

        result = False


        try:
            self._odoo = odoorpc.ODOO(self._server, port=self._port)
            result = True
        except Exception as ex:
            print ex

        return result


    def _login(self):
        """ Tries to login with user and password or renew session
        """
        result = False

        self._odoo.logout()

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

        return result


    def _logout(self):
        """ Loggout from Odoo server """
        self._odoo.logout()

    def _search_one(self):
        domain = []

        if self._id:
            domain.append(('id', '=', self._id))

        if self._title:
            domain.append(('name', 'ilike', self._title))

        test_ids = self._odoo.env['at.test'].search(domain)

        return test_ids[0] if test_ids else 0


    def _download_report(self, report_id):
        print self._report
        return self._odoo.report.download(
            self._report,
            [report_id]
        )


    def _save_report(self, report):
        with open(self._output, 'wb') as report_file:
            report_file.write(report.read())


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


        if (self._id or self._title) and self._connect():

            if self._login():

                report_id = self._search_one()
                if report_id > 0:
                    report = self._download_report(report_id)

                    self._save_report(report)

                self._logout()

        else:
            print u'Please type an ID or a title, see --help'

        sys.exit(result)



# --------------------------- SCRIPT ENTRY POINT ------------------------------

App().main()


