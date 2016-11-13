# -*- coding: utf-8 -*-
#pylint: disable=I0011,R0201,R0903,W0703
""" Reads a TXT file with questions and answers and creates an SQL script
to fill academy_test tables.
"""

# --------------------------- REQUIRED LIBRARIES ------------------------------

import argparse
import os
import re
import locale

from datetime import datetime

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
        self._file = None
        self._out = None
        self._question_sequence = 0
        self._answer_sequence = 0
        self._sql = u''
        self._cp = locale.getpreferredencoding()
        self._name = None
        self._description = None
        self._preamble = None

    def _argparse(self):
        """ Detines an user-friendly command-line interface and proccess its
        arguments.
        """

        # STEP 1: Define the arbument parser
        description = u'Create SQL script from text file'
        parser = argparse.ArgumentParser(description)

        # STEP 2: Determine positional arguments
        parser.add_argument('file', metavar='file', type=str,
                            help='in text file path')

        # STEP 3: Determine non positional arguments
        parser.add_argument('-o', '--out', type=str, dest='out',
                            default=None, help='out SQL file path')

        parser.add_argument('-n', '--name', type=str, dest='name',
                            default=datetime.now().strftime("AUTO %d/%m/%Y %H:%M:%S"),
                            help='name for test')

        parser.add_argument('-d', '--desc', type=str, dest='description',
                            default=u'',
                            help='description for test')

        parser.add_argument('-p', '--preamble', action='store_true',
                            default=False, help='unknown lines as preamble')

        args = parser.parse_args()

        self._file = os.path.abspath(args.file.decode(self._cp, errors='replace'))
        if args.out:
            self._out = os.path.abspath(args.out.decode(self._cp, errors='replace'))
        self._name = args.name.decode(self._cp, errors='replace')
        self._description = args.description.decode(self._cp, errors='replace')
        self._preamble = args.preamble

    def _is_question(self, line):
        """ Check if line is for question ^[0-9]+
        """
        return bool(re.match(r'^[0-9]{1,2}[\)\.\- ]+.*$', line, re.IGNORECASE))

    def _new_question(self, line, preamble=u''):
        """ Creates new question INSERT script for line
        """

        self._question_sequence += 1
        self._answer_sequence = 0

        line = line.replace('\'', '\'\'')

        return u"""
            WITH tmp AS (
                INSERT INTO "public"."at_question" (
                    "name",
                    "description",
                    "preamble",
                    "create_uid",
                    "create_date",
                    "write_uid",
                    "write_date",
                    "active",
                    "at_topic_id",
                    "at_level_id"
                ) VALUES (
                    '{}',
                    NULL,
                    '{}',
                    '1',
                    now()::TIMESTAMP (0),
                    '1',
                    now()::TIMESTAMP (0),
                    't',
                    (SELECT id FROM "public"."at_topic" WHERE NAME = 'TEST2SQL'),
                    '4'
                ) RETURNING "id"
            ) INSERT INTO at_category_at_question_rel
                (at_category_id, at_question_id)
            VALUES
                ( (SELECT id FROM "public"."at_category" WHERE NAME = 'TEST2SQL'), (SELECT id FROM tmp));
        """.format(line, preamble)

    def _is_answer(self, line):
        """ Check if line is for question ^[ABCDabcd]+
        """
        return bool(re.match(r'^[abcdx][\)\.\- ]+.*$', line, re.IGNORECASE))


    def _new_answer(self, line, is_correct=False):
        """ Creates new answer INSERT script for line
        """

        self._answer_sequence += 1

        line = line.replace('\'', '\'\'')

        return u"""
            INSERT INTO "public"."at_answer" (
                "sequence",
                "name",
                "description",
                "create_uid",
                "create_date",
                "write_uid",
                "write_date",
                "is_correct",
                "at_question_id",
                "active"
            ) VALUES (
                {},
                '{}',
                NULL,
                '1',
                now()::TIMESTAMP (0),
                '1',
                now()::TIMESTAMP (0),
                {},
                (SELECT "id" FROM at_question ORDER BY ID DESC LIMIT 1),
                't'
            );
        """.format(self._answer_sequence, line, u'true' if is_correct else u'false')


    def _register_question(self, question):
        """ Add INSERT scripts to the general script
        """
        self._sql += (question)

    def _register_answer(self, answer):
        """ Add INSERT scripts to the general script
        """
        self._sql += (answer)

    def _clear_question(self, line):
        """ Cliear questions
        """
        return re.search(r'^[0-9]{1,2}[\)\.\- ]+(.*)$', line).group(1)

    def _clear_answer(self, line):
        """ Cliear questions
        """
        is_correct = line and line[0].lower() == 'x'
        return re.search(r'^[abcdxABCDX]{1,2}[\)\.\- ]+(.*)$', line).group(1), is_correct

    def _register_topic(self):
        """ SQL to ensure topic
        """

        self._sql += u"""
        INSERT INTO "public"."at_topic" (
            "name",
            "description",
            "create_uid",
            "create_date",
            "write_uid",
            "write_date",
            "active"
        )
        SELECT
            'TEST2SQL',
            'Test generados con la herramienta TEST2SQL',
            '1',
            now()::TIMESTAMP (0),
            '1',
            now()::TIMESTAMP (0),
            't'
        WHERE
            NOT EXISTS (
                    SELECT id FROM "public"."at_topic" WHERE NAME = 'TEST2SQL'
        );
        """

    def _register_category(self):
        """ SQL to ensure category
        """

        self._sql += u"""
        INSERT INTO "public"."at_category" (
            "name",
            "description",
            "create_uid",
            "create_date",
            "write_uid",
            "write_date",
            "sequence",
            "active",
            "at_topic_id"
        )
        SELECT
            'TEST2SQL',
            'Test generados con la herramienta TEST2SQL',
            1,
            now()::TIMESTAMP (0),
            1,
            now()::TIMESTAMP (0),
            1024,
            't',
            (SELECT id FROM "public"."at_topic" WHERE NAME = 'TEST2SQL' )
        WHERE
                NOT EXISTS (
                                SELECT id FROM "public"."at_category" WHERE NAME = 'TEST2SQL'
        );
        """


    def _register_test(self):
        """ SQL to create test """

        self._sql += u"""
             WITH newtest AS (
                INSERT INTO "public"."at_test" (
                    "name",
                    "description",
                    "create_date",
                    "create_uid",
                    "write_uid",
                    "write_date",
                    "active"
                )
                VALUES
                    (
                        '{}',
                        '{}',
                        now()::TIMESTAMP (0),
                        '1',
                        '1',
                        now()::TIMESTAMP (0),
                        't'
                    ) RETURNING ID
            ) INSERT INTO "public"."at_test_at_question_rel" (
                "at_test_id",
                "at_question_id",
                "sequence",
                "create_uid",
                "create_date",
                "write_uid",
                "write_date"
            ) SELECT
                (SELECT ID FROM newtest) AS at_test_id,
                ID AS at_question_id,
                ROW_NUMBER () OVER () AS "secuence",
                1 AS create_uid,
                now()::TIMESTAMP (0) AS create_date,
                1 AS write_uid,
                now()::TIMESTAMP (0) AS write_date
            FROM
                at_question
            ORDER BY
                ID DESC
            LIMIT {};


        """.format(self._name, self._description, self._question_sequence)

    def _txt2sql(self):
        """ Main method docstring
        """

        self._register_topic()
        self._register_category()

        try:
            preamble = u''

            with open(self._file, 'r') as finput: #open the file
                lines = finput.readlines()
                for line_raw in lines:
                    line = line_raw.decode('utf-8', errors='replace')
                    if self._is_question(line):
                        line = self._clear_question(line)
                        question = self._new_question(line, preamble)
                        preamble = u''
                        if question:
                            self._register_question(question)
                    elif self._is_answer(line):
                        line, is_correct = self._clear_answer(line)
                        answer = self._new_answer(line, is_correct)
                        if answer:
                            self._register_answer(answer)
                    elif self._preamble and len(line) > 3:
                        preamble += line
                    else:
                        print u'Skip line %s' % line

        except Exception as ex:
            print ex
        else:
            self._register_test()
            self._sql = u'END; BEGIN; {} END;'.format(self._sql)
            if self._out:
                with open(self._out, 'w') as foutput: #open the file
                    foutput.write(self._sql.encode('utf-8', errors='replace'))
                print u'File %s has been written' % self._out
            else:
                print self._sql.encode(self._cp, errors='replace')

    def main(self):
        """ The main application behavior, this method should be used to
        start the application.
        """

        self._argparse()

        self._txt2sql()


# --------------------------- SCRIPT ENTRY POINT ------------------------------

App().main()
