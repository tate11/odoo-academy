# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Name of model

This module contains unit test for academy.training.session.wizard model
"""

from logging import getLogger
from datetime import date, timedelta

# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)


# pylint: disable=locally-disabled, E0401
from openerp.tests.common import TransactionCase
from openerp import fields


# pylint: disable=locally-disabled, R0904, C0103, W0212, C0111
class TestAcademyTrainingSessionWizard(TransactionCase):
    """ This class contains the unit tests for 'test.academy.training.session.wizard'.

        Tests:
          - item_name: Checks if the item_name works properly
    """

    def setUp(self):
        """ Prepair unit tests """

        super(TestAcademyTrainingSessionWizard, self).setUp()

        self._wizard_obj = self.env['academy.training.session.wizard']
        self._start_date = date(2018, 10, 1)


    # pylint: disable=locally-disabled, W0102
    def _new_wizard(self, wdata={}, ldata={}):
        start_date = fields.Date.to_string(self._start_date)

        values = {
            'following' : ldata.get('following', False),
            'start_date': ldata.get('start_date', start_date),
            'start_time': ldata.get('start_time', 9.0),
            'duration'  : ldata.get('duration', 5.0),
            'maximum'   : ldata.get('maximum', 5.0),
            'incomplete': ldata.get('incomplete', 'next')
        }

        wizard_set = self._wizard_obj .create(wdata)

        line_set = wizard_set.wizard_line_ids.sorted( \
            key=lambda p: (p.training_module_id.sequence, p.sequence))
        line_set[0].update(values)

        return wizard_set, line_set


    @staticmethod
    def _line_headers():
        return (
            'Training Unit',
            'Imparted',
            'Following',
            'Start date',
            'Start time',
            'Duration',
            'Maximum',
            'Incomplete'
        )

    @staticmethod
    def _lesson_headers():
        return (
            'Code',
            'Action',
            'Module',
            'Start_date',
            'Duration'
        )


    @staticmethod
    def _line_to_tuple(line):
        return (
            str(line.training_unit_id.name),
            str(line.imparted),
            str(line.following),
            str(line.start_date),
            str(line.start_time),
            str(line.duration),
            str(line.maximum),
            str(line.incomplete)
        )


    @staticmethod
    def _lesson_to_tuple(lesson):
        return (
            str(lesson.code),
            str(lesson.training_action_id.id),
            str(lesson.training_module_id.id),
            str(lesson.start_date),
            str(lesson.duration)
        )


    def _build_line(self, line=False):
        patern = '{:20}  {:^8}  {:^9}  {:^10}  {:^10}  {:^8}  {:^7}  {:^10}'

        if line:
            result = patern.format(*self._line_to_tuple(line))
        else:
            result = patern.format(*self._line_headers())

        return result



    def _build_lesson(self, lesson=False):
        patern = '{:10}  {:^10}  {:^10}  {:^10}  {:^10}'

        if lesson:
            result = patern.format(*self._lesson_to_tuple(lesson))
        else:
            result = patern.format(*self._lesson_headers())

        return result


    def _log_wizard_data(self, wizard_set, msg='', result=None):
        msg = '{}'.format(msg)

        wizard_set.ensure_one()

        msg = msg + '\nInterval       : ' + str(wizard_set.interval)
        msg = msg + '\nRrule type     : ' + wizard_set.rrule_type
        if wizard_set.rrule_type == 'weekly':
            msg = msg + '\nWeekdays       : ' + str(wizard_set._get_weekdays())
        elif wizard_set.rrule_type == 'monthly':
            msg = msg + '\nMonth_by       : ' + wizard_set.month_by
            if wizard_set.month_by == 'date':
                msg = msg + '\n  Month day    : ' + str(wizard_set.day)
            else:
                msg = msg + '\n  Month byday  : ' + wizard_set.byday
                msg = msg + '\n  weeklist     : ' + wizard_set.week_list

        line_set = wizard_set.wizard_line_ids.sorted( \
            key=lambda p: (p.training_module_id.sequence, p.sequence))

        if line_set:
            msg = msg + '\n' + self._build_line()
            for line in line_set:
                msg = msg + '\n' + self._build_line(line)

        if wizard_set.training_lesson_ids:
            msg = msg + '\n' + self._build_lesson()
            for lesson in wizard_set.training_lesson_ids:
                msg = msg + '\n' + self._build_lesson(lesson)

        if result:
            msg = msg + '\n' + result

        return msg


    def test__process_line_1(self):



        expected = (self._start_date + timedelta(days=1), 0)

        wizard_set, line_set = self._new_wizard()
        result = wizard_set._process_line(line_set[0], self._start_date, 0)
        lesson_set = wizard_set.training_lesson_ids

        msg = self._log_wizard_data(
            wizard_set,
            '_process_line(line_set[0], {}, {})'.format(self._start_date, 0),
            'Result: {} - Expected: {}'.format(result, expected)
        )
        self.assertTrue(len(lesson_set) == 1 and result == expected, msg)


        expected = (self._start_date + timedelta(days=1), 1)

        wizard_set, line_set = self._new_wizard()
        result = wizard_set._process_line(line_set[0], self._start_date, 1)
        lesson_set = wizard_set.training_lesson_ids

        msg = self._log_wizard_data(
            wizard_set,
            '_process_line(line_set[0], {}, {})'.format(self._start_date, 1),
            'Result: {} - Expected: {}'.format(result, expected)
        )
        self.assertTrue(len(lesson_set) == 2 and result == expected, msg)



