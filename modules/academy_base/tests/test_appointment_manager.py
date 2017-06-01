#pylint: disable=I0011,C0111,F0401,C0103,R0914,W0611
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################


from openerp.tests.common import TransactionCase
from logging import getLogger
from datetime import date, datetime, timedelta
import os
from sys import maxint ## Needed to configure, See ``setUp`` method
from ast import literal_eval
import json
from pprint import pprint


_logger = getLogger(__name__)


Mo = 0
Tu = 1
We = 2
Th = 3
Fr = 4
Sa = 5
Su = 6

class AppointmentManager(TransactionCase):
    """ This class contains the unit tests for 'model.name'.

        Tests:
          - item_name: Checks if the item_name works properly
    """

    _model_name = 'appointment.manager'

    @staticmethod
    def _str2date(in_str, pattern='%d/%m/%Y'):
        """ Returns a date objet from string formated with pattern"""
        return datetime.strptime(in_str, pattern).date()

    def setUp(self):
        """ Prepares AppointmentManager objet to perform unit tests """

        # IMPORTANT: set to maxint to perform full test
        self._max_iterations = 15000

        json_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(json_path, u'test_appointment_manager.json')

        with open(json_path) as json_file:
            self._data = json.load(json_file)

        # STEP 1: merge holiday dates
        self._holidays = []
        for year_list in self._data['holidays'].values():
            for date_str in year_list:
                date_value = datetime.strptime(date_str, '%d/%m/%Y').date()
                self._holidays.append(date_value)

        # STEP 2: Load next_day


        super(AppointmentManager, self).setUp()

    def test_range(self):
        """ Checks if the range works properly
        """

        model_obj = self.env[self._model_name]
        start = self._str2date(self._data['next_day']['start'])
        final_date = self._str2date(self._data['next_day']['end'])

        # STEP 1: rrule_type = 'daily'
        expected = [
            self._str2date(str_date) \
            for str_date in self._data['next_day']['results']
        ]
        print 'range', start, 'daily', 1, final_date, ('holidays %d' % len(self._holidays)), None

        result = model_obj.range(
            start,
            'daily',
            1,
            final_date,
            self._holidays,
            None
        )

        self.assertListEqual(
            expected,
            result,
            msg='test_range for rrule_type = ''daily'' fail'
        )

    def test_WorkDays(self):
        """ Checks if method WorkDays works properly """

        model_obj = self.env[self._model_name]

        base = date(2017, 5, 22)
        #w1 = [base - timedelta(8 - offset) for offset in range(1, 8)]
        w2 = [base + timedelta(offset) for offset in range(0, 7)]
        w3 = [w2[6] + timedelta(offset) for offset in range(1, 8)]

        # STEP 1: Same day, workday
        _logger.info('WORKDAYS - Same day, workday')
        self.assertIs(
            model_obj.WorkDays(w2[Mo], w2[Mo]),
            1,
            msg='Same day, workday should be Zero'
        )

        # STEP 2: Same day, weekend
        _logger.info('WORKDAYS - Same day, weekend')
        self.assertIs(
            model_obj.WorkDays(w2[Su], w2[Su]),
            0,
            msg='Same day, weekend should be Zero'
        )

        # STEP 3: Same day, holiday
        _logger.info('WORKDAYS - Same day, holiday')
        self.assertIs(
            model_obj.WorkDays(w2[Mo], w2[Mo], holidays=w2[Mo]),
            0,
            msg='Same day, holiday should be Zero'
        )

        # STEP 4: Sunday to monday
        _logger.info('WORKDAYS - Sunday to monday')
        self.assertIs(
            model_obj.WorkDays(w2[Su], w3[Mo]),
            1,
            msg='Sunday to monday should be one'
        )

        # STEP 5: Sunday to monday, monday holiday
        _logger.info('WORKDAYS - Sunday to monday, monday holiday')
        self.assertIs(
            model_obj.WorkDays(w2[Su], w3[Mo], holidays=w3[Mo]),
            0,
            msg='Sunday to monday, monday holiday, should be zero'
        )

        # STEP 6: Friday to saturday
        _logger.info('WORKDAYS - Friday to saturday')
        self.assertIs(
            model_obj.WorkDays(w2[Fr], w2[Sa]),
            1,
            msg='Friday to saturday should be one'
        )

        # STEP 7: Friday to saturday, friday holiday
        _logger.info('WORKDAYS - Friday to saturday, friday holiday')
        self.assertIs(
            model_obj.WorkDays(w2[Fr], w2[Sa], holidays=w2[Fr]),
            0,
            msg='Friday to saturday, friday holiday, should be zero'
        )

        # STEP 8: Workdays beetween monday and sunday using each one day
        _logger.info('WORKDAYS - Workdays beetween monday and sunday using each one day')
        # in week as unique non working day
        for index in range(1, 8):
            wd = range(1, 8)
            wd.remove(index)

            result = model_obj.WorkDays(w2[Mo], w2[Su], wd)
            self.assertIs(
                int(result) - 6,
                0,
                msg='WorkDays({}, {}, {}, None) -> {} / 6'.format(
                    w2[Mo], w2[Su], wd, result
                )
            )

        # STEP 9: Compare results with Excel for calendar of the Vigo for 2017
        _logger.info(
            'WORKDAYS - Compare results with Excel for calendar of the ' \
            'Vigo city for year 2017'
        )
        holidays = [
            date(2017, 1, 1),
            date(2017, 1, 6),
            date(2017, 4, 14),
            date(2017, 5, 1),
            date(2017, 8, 15),
            date(2017, 10, 12),
            date(2017, 11, 1),
            date(2017, 12, 6),
            date(2017, 12, 8),
            date(2017, 12, 25),
            date(2017, 3, 28),
            date(2017, 8, 16),
            date(2017, 4, 13),
            date(2017, 5, 17),
            date(2017, 7, 25),
        ]

        excel_results_path = os.path.dirname(os.path.abspath(__file__))
        excel_results_path = os.path.join(excel_results_path, u'networkdays.excel')

        with open(excel_results_path, mode='r') as infile:
            content = infile.readlines()

        row_count = 0
        for line in [x.strip() for x in content]:
            values = literal_eval(line)
            dt1 = datetime.strptime(values[0], '%d/%m/%Y')
            dt2 = datetime.strptime(values[1], '%d/%m/%Y')
            right_value = values[2]
            result = model_obj.WorkDays(dt1, dt2, holidays=holidays)
            self.assertIs(
                int(result) - int(right_value),
                0,
                msg='WorkDays({}, {}) should be {}'.format(dt1, dt2, right_value)
            )
            row_count = row_count + 1
            if row_count >= self._max_iterations:
                break

        _logger.info('WORKDAY - Performed %d comparisions', row_count)


    def _test_WorkDay(self):
        #pylint: disable=I0011,R0915
        """ Checks if method WorkDay works properly """

        model_obj = self.env[self._model_name]

        base = date(2017, 5, 22)
        w1 = [base - timedelta(8 - offset) for offset in range(1, 8)]
        w2 = [base + timedelta(offset) for offset in range(0, 7)]
        w3 = [w2[6] + timedelta(offset) for offset in range(1, 8)]

        # STEP 1: Move forward 0 days from workday
        _logger.info('WORKDAY - Move forward 0 days from workday')
        result = model_obj.WorkDay(w2[Mo], 0)
        self.assertTrue(
            result == w2[Mo],
            msg='Move forward 0 days from workday must return same day'
        )

        # STEP 2: Move forward 0 days from weekend
        _logger.info('WORKDAY - Move forward 0 days from weekend')
        result = model_obj.WorkDay(w2[Su], 0)
        self.assertTrue(
            result == w2[Su],
            msg='Move forward 0 days from weekend must return same day'
        )

        # STEP 3: Move forward 0 days from holiday
        _logger.info('WORKDAY - Move forward 0 days from holiday')
        result = model_obj.WorkDay(w2[Mo], 0, holidays=w2[Mo])
        self.assertTrue(
            result == w2[Mo],
            msg='Move forward 0 days from holiday must return same day'
        )

        # STEP 4: Move forward 1 days from workday to workday
        _logger.info('WORKDAY - Move forward 1 days from workday to workday')
        result = model_obj.WorkDay(w2[Mo], 1)
        self.assertTrue(
            result == w2[Tu],
            msg='Move forward 1 days from workday to workday must return next day'
        )

        # STEP 5: Move forward 1 days from weekend to workday
        _logger.info('WORKDAY - Move forward 1 days from weekend to workday')
        result = model_obj.WorkDay(w2[Su], 1)
        self.assertTrue(
            result == w3[Mo],
            msg='Move forward 1 days from weekend to workday must return next day'
        )

        # STEP 6: Move forward 1 days from holiday to workday
        _logger.info('WORKDAY - Move forward 1 days from holiday to workday')
        result = model_obj.WorkDay(w2[Mo], 1, holidays=w2[Mo])
        self.assertTrue(
            result == w2[Tu],
            msg='Move forward 1 days from holiday to workday must return next day'
        )

        # STEP 7: Move forward 1 days from workday to weekend
        _logger.info('WORKDAY - Move forward 1 days from workday to weekend')
        result = model_obj.WorkDay(w2[Fr], 1)
        self.assertTrue(
            result == w3[Mo],
            msg='Move forward 1 days from workday to weekend must return next week'
        )

        # STEP 8: Move forward 1 days from workday to holiday
        _logger.info('WORKDAY - Move forward 1 days from workday to holiday')
        result = model_obj.WorkDay(w2[Th], 1, holidays=w2[Fr])
        self.assertTrue(
            result == w3[Mo],
            msg='Move forward 1 days from workday to holiday must jump over holiday'
        )

        # STEP 10: Move backward 1 days from workday to workday
        _logger.info('WORKDAY -  Move backward 1 days from workday to workday')
        result = model_obj.WorkDay(w2[Tu], -1)
        self.assertTrue(
            result == w2[Mo],
            msg='Move backward 1 days from workday to workday must return same day'
        )

        # STEP 11: Move backward 1 days from weekend to workday
        _logger.info('WORKDAY -  Move backward 1 days from weekend to workday')
        result = model_obj.WorkDay(w2[Sa], -1)
        self.assertTrue(
            result == w2[Fr],
            msg='Move backward 1 days from workday to workday must return workday'
        )

        # STEP 12: Move backward 1 days from holiday to workday
        _logger.info('WORKDAY -  Move backward 1 days from holiday to workday')
        result = model_obj.WorkDay(w2[Tu], -1, holidays=w2[Tu])
        self.assertTrue(
            result == w2[Mo],
            msg='Move backward 1 days from workday to workday must return workday'
        )

        # STEP 14: Move backward 1 days from workday to weekend
        _logger.info('WORKDAY -  Move backward 1 days from workday to weekend')
        result = model_obj.WorkDay(w2[Mo], -1)
        self.assertTrue(
            result == w1[Fr],
            msg='Move backward 1 days from workday to workday must return jump over weekend'
        )

        # STEP 15: Move backward 1 days from workday to holiday
        _logger.info('WORKDAY -  Move backward 1 days from workday to holiday')
        result = model_obj.WorkDay(w2[Tu], -1, holidays=w2[Mo])
        self.assertTrue(
            result == w1[Fr],
            msg='Move backward 1 days from workday to workday must jump over holiday'
        )

       # STEP 9: Compare results with Excel for calendar of the Vigo for 2017
        _logger.info(
            'WORKDAY - Compare results with Excel for calendar of the ' \
            'Vigo city for year 2017'
        )


        holidays = [
            date(2017, 1, 1),
            date(2017, 1, 6),
            date(2017, 4, 14),
            date(2017, 5, 1),
            date(2017, 8, 15),
            date(2017, 10, 12),
            date(2017, 11, 1),
            date(2017, 12, 6),
            date(2017, 12, 8),
            date(2017, 12, 25),
            date(2017, 3, 28),
            date(2017, 8, 16),
            date(2017, 4, 13),
            date(2017, 5, 17),
            date(2017, 7, 25),
        ]

        excel_results_path = os.path.dirname(os.path.abspath(__file__))
        excel_results_path = os.path.join(excel_results_path, u'networkday.excel')

        with open(excel_results_path, mode='r') as infile:
            content = infile.readlines()

        row_count = 0
        for line in [x.strip() for x in content]:
            values = literal_eval(line)
            dt1 = datetime.strptime(values[0], '%d/%m/%Y')
            days = values[1]
            expected = datetime.strptime(values[2], '%d/%m/%Y').date()

            result = model_obj.WorkDay(dt1, days, holidays=holidays)
            self.assertTrue(
                result == expected,
                msg='WorkDay({}, {}) should be {} not {}'.format(dt1, days, expected, result)
            )
            row_count = row_count + 1
            if row_count >= self._max_iterations:
                break


        _logger.info('WORKDAY - Performed %d comparisions', row_count)

