# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0703,R0903,R0902
""" Transforms YAML tests made for Moodle in Markdown tests made for Odoo
"""


# --------------------------- REQUIRED LIBRARIES ------------------------------


import argparse
import io, os
import pprint
import locale
import sys
import regex

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
            cls.__instance.name = "Transform tests"
        return cls.__instance


    def __init__(self):
        self._cp = locale.getpreferredencoding()
        self._file = None
        self._encode = None
        self._out = None


    def _argparse(self):
        """ Detines an user-friendly command-line interface and proccess its
        arguments.
        """

        description = u'Transform Moodle YAML test files to Odoo Markdown test files'

        parser = argparse.ArgumentParser(description)
        parser.add_argument('file', metavar='file', type=str,
                             help=u'path of the resource file will be transformed')

        parser.add_argument('-e', '--encode', type=str, dest='encode',
                            default=u'utf-8',
                            help=u'Character encoding will be used to read and write files')

        parser.add_argument('-o', '--out', type=str, dest='out',
                            default='outfile.txt',
                            help=u'Path with filename will be used to save new file')

        args = parser.parse_args()
        self._file = os.path.abspath(args.file)
        self._encode = args.encode
        self._out = args.out


    def _transform(self):
        """ Performs the required operations """
        lines = []
        newlines = []
        linebreaks = 0
        
        with io.open(self._file, encoding=self._encode) as finput: 
            lines = finput.readlines()

        for index in range(0, len(lines)):
            if lines[index][0:2] == '~ ':
                pattern = regex.compile(r'^~ +')
                lines[index] = pattern.sub('a) ', lines[index])
            elif lines[index][0:2] == '= ':
                pattern = regex.compile(r'^= +')
                lines[index] = pattern.sub('x) ', lines[index])
            else:
                pattern = regex.compile(r'(^ *\} *)|( *\{ *$)')
                lines[index] = pattern.sub(r'', lines[index])

                pattern = regex.compile(r'^.*\$CATEGORY\:.*')
                lines[index] = pattern.sub(r'', lines[index])

                if len(lines[index]) > 1:
                    lines[index] = '1. ' + lines[index]

            pattern = regex.compile(r'[ \t]+')
            lines[index] = pattern.sub(r' ', lines[index])

            pattern = regex.compile(r'\.+$')
            lines[index] = pattern.sub(r'', lines[index])

        with io.open(self._out, 'w+', encoding='utf-8') as foutput: 
            foutput.writelines(lines)


    def main(self):
        """ The main application behavior, this method should be used to
        start the application.
        """
        result = -1

        self._argparse()

        result = self._transform()

        sys.exit(result)



# --------------------------- SCRIPT ENTRY POINT ------------------------------

App().main()


