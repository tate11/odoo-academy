# -*- coding: utf-8 -*-
#pylint: disable=I0011
""" This module connects to the OdooERP academy modules using RPC to get and
show stored information from console.
"""

# --------------------------- REQUIRED LIBRARIES ------------------------------

import argparse


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
        pass

    def _argparse(self):
        """ Detines an user-friendly command-line interface and proccess its
        arguments.
        """

        # STEP 1: Define the arbument parser
        description = u'Odoo academy client'
        parser = argparse.ArgumentParser(description)

        # STEP 2: Determine positional arguments
        # parser.add_argument('command', metavar='command', type=str,
        #                     help='description for comamnd')

        # STEP 3: Determine non positional arguments
        # parser.add_argument('-m', '--modifier', type=str, dest='modifier',
        #             choices=['one', 'two', 'tree'], default='day',
        #             help='description for modifier')

        args = parser.parse_args()


    def _execute_commands()(self):
        """ Main method docstring
        """

        try:



        except Exception as ex:
            print ex
        else:
            print u'New file %s has been written.' % new_path

    def main(self):
        """ The main application behavior, this method should be used to
        start the application.
        """

        self._argparse()

        self._execute_commands()


# --------------------------- SCRIPT ENTRY POINT ------------------------------

App().main()
# -*- coding: utf-8 -*-
#pylint: disable=I0011
""" This module connects to the OdooERP academy modules using RPC to get and
show stored information from console.
"""

# --------------------------- REQUIRED LIBRARIES ------------------------------

import argparse


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
        pass

    def _argparse(self):
        """ Detines an user-friendly command-line interface and proccess its
        arguments.
        """

        # STEP 1: Define the arbument parser
        description = u'Odoo academy client'
        parser = argparse.ArgumentParser(description)

        # STEP 2: Determine positional arguments
        # parser.add_argument('command', metavar='command', type=str,
        #                     help='description for comamnd')

        # STEP 3: Determine non positional arguments
        # parser.add_argument('-m', '--modifier', type=str, dest='modifier',
        #             choices=['one', 'two', 'tree'], default='day',
        #             help='description for modifier')

        args = parser.parse_args()


    def _execute_commands()(self):
        """ Main method docstring
        """

        try:



        except Exception as ex:
            print ex
        else:
            print u'New file %s has been written.' % new_path

    def main(self):
        """ The main application behavior, this method should be used to
        start the application.
        """

        self._argparse()

        self._execute_commands()


# --------------------------- SCRIPT ENTRY POINT ------------------------------

App().main()
