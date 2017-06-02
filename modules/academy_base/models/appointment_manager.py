#pylint: disable=I0011,C0111,W0611,F0401,C0103,R0903,C0302,W0212,R0201,R0913
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger

from datetime import date, datetime, timedelta
from pytz import timezone, utc
from sys import maxint
from calendar import monthrange


_logger = getLogger(__name__)


class AppointmentManager(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'appointment.manager'
    _description = u'Appointment manager'

    _rec_name = 'start'
    _order = 'start ASC'


    _kill_switch = 9130 # Maximum number of iterations in loop (25 years)


    # ---------------------------- ENTITY FIELDS ------------------------------


    start = fields.Datetime(
        string='Start',
        required=True,
        readonly=True,
        index=False,
        default=lambda self: self._utc_o_clock(),
        help='Start date of an event, without time for full days events'
    )

    stop = fields.Datetime(
        string='End',
        required=True,
        readonly=True,
        index=False,
        default=lambda self: self._utc_o_clock(),
        help='Stop date of an event, without time for full days events'
    )

    allday = fields.Boolean(
        string='All day',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check if appointment lasts all day'
    )

    duration = fields.Float(
        string='Duration',
        required=True,
        readonly=False,
        index=False,
        default=1.0,
        digits=(16, 2),
        help='Length of appointment'

    )

    recurrency = fields.Boolean(
        string='Recurrency',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Check for activate recurrency'
    )

    final_date = fields.Date(
        string='Final date',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._utc_o_clock(dateonly=True),
        help=False
    )

    interval = fields.Integer(
        string='Repeat Every',
        required=False,
        readonly=False,
        index=False,
        default=1,
        help='Repeat every (Days/Week/Month/Year)'
    )

    rrule_type = fields.Selection(
        string='Recurrency',
        required=False,
        readonly=False,
        index=False,
        default='weekly',
        help='Let the event automatically repeat at that interval',
        selection=[
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)'),
        ],
        #states={'done': [('readonly', True)]}
    )

    mo = fields.Boolean(
        string='Monday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for monday"
    )

    tu = fields.Boolean(
        string='Tuesday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for tuesday"
    )

    we = fields.Boolean(
        string='Wednesday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for wednesday"
    )

    th = fields.Boolean(
        string='Thursday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for Thursday"
    )

    fr = fields.Boolean(
        string='Friday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for friday"
    )

    sa = fields.Boolean(
        string='Saturday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help="Check for saturday"
    )

    su = fields.Boolean(
        string='Sunday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help="Check for sunday"
    )

    end_type = fields.Selection(
        string='Recurrence termination',
        required=False,
        readonly=False,
        index=False,
        default='count',
        help='Choose the recurrence termination',
        selection=[
            ('count', 'Number of repetitions'),
            ('stop_date', 'End date')
        ]
    )

    count = fields.Integer(
        string='Repeat',
        required=False,
        readonly=False,
        index=False,
        default=4,
        help='Repeat x times'
    )

    month_by = fields.Selection(
        string='Option',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Choose an option',
        selection=[
            ('date', 'Date of month'),
            ('day', 'Day of month')
        ]
    )

    day = fields.Integer(
        string='Date of month',
        required=False,
        readonly=False,
        index=False,
        default=1,
        help='Enter day of month'
    )

    week_list = fields.Selection(
        string='Weekday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help=False,
        selection=[
            ('MO', 'Monday'),
            ('TU', 'Tuesday'),
            ('WE', 'Wednesday'),
            ('TH', 'Thursday'),
            ('FR', 'Friday'),
            ('SA', 'Saturday'),
            ('SU', 'Sunday')
        ]
    )

    byday = fields.Selection(
        string='Byday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help=False,
        selection=[
            ('1', 'First'),
            ('2', 'Second'),
            ('3', 'Third'),
            ('4', 'Fourth'),
            ('5', 'Fifth'),
            ('-1', 'Last')
        ]
    )


    # --------------------------- COMPUTED FIELDS -----------------------------


    start_datetime = fields.Datetime(
        string='Start time',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._utc_o_clock(),
        help='Start datetime of the first appointment',
        compute=lambda self: self._compute_dates(),
        inverse=lambda self: self._inverse_dates(),
        store=True
    )

    stop_datetime = fields.Datetime(
        string='End time',
        required=False,
        readonly=True,
        index=False,
        default=lambda self: self._utc_o_clock(offset=1),
        help='End datetime of the first appointment',
        compute=lambda self: self._compute_dates(),
        inverse=lambda self: self._inverse_dates(),
        store=True
    )

    start_date = fields.Date(
        string='Start date',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._utc_o_clock(dateonly=True),
        help='Start date',
        compute=lambda self: self._compute_dates(),
        inverse=lambda self: self._inverse_dates(),
        store=True
    )

    stop_date = fields.Date(
        string='End date',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._utc_o_clock(dateonly=True),
        help='End date',
        compute=lambda self: self._compute_dates(),
        inverse=lambda self: self._inverse_dates(),
        store=True
    )


    # ------------------ COMPUTED FIELD METHODS AND EVENTS --------------------


    @api.multi
    @api.depends('allday', 'start', 'stop')
    def _compute_dates(self):

        for appointment in self:
            if appointment.allday:
                appointment.start_date = appointment.start
                appointment.start_datetime = False
                appointment.stop_date = appointment.stop
                appointment.stop_datetime = False

                appointment.duration = 0.0
            else:
                appointment.start_date = False
                appointment.start_datetime = appointment.start
                appointment.stop_date = False
                appointment.stop_datetime = appointment.stop

                appointment.duration = self._get_duration(appointment.start, appointment.stop)

    @api.multi
    def _inverse_dates(self):
        for appointment in self:
            if appointment.allday:
                tz = timezone(self.env.user.tz) if self.env.user.tz else utc

                enddate = fields.Datetime.from_string(appointment.stop_date)
                enddate = tz.localize(enddate)
                enddate = enddate.replace(hour=18)
                enddate = enddate.astimezone(utc)
                appointment.stop = fields.Datetime.to_string(enddate)

                startdate = fields.Datetime.from_string(appointment.start_date)
                startdate = tz.localize(startdate)  # Add "+hh:mm" timezone
                startdate = startdate.replace(hour=8)  # Set 8 AM in localtime
                startdate = startdate.astimezone(utc)  # Convert to UTC
                appointment.start = fields.Datetime.to_string(startdate)

                appointment.duration = 0.0
            else:
                appointment.start = appointment.start_datetime

                start = fields.Datetime.from_string(appointment.start_datetime)
                appointment.stop = fields.Datetime.to_string(
                    start + timedelta(hours=appointment.duration))


    # -------------------------------- CRUD -----------------------------------


    @api.model
    def create(self, values):
        """
            Create a new record for a model AppointmentManager
            @param values: provides a data for new record

            @return: returns a id of new record
        """

        # Ensure duration is Zero when allday is set to true
        if values.get('allday', False):
            values['duration'] = 0.0

        return super(AppointmentManager, self).create(values)

    @api.multi
    def write(self, values):
        """
            Update all record(s) in recordset, with new value comes as {values}
            return True on success, False otherwise

            @param values: dict of new values to be set

            @return: True on success, False otherwise
        """

        # Ensure duration is Zero when allday is set to true
        if values.get('allday', False):
            values['duration'] = 0.0

        return super(AppointmentManager, self).write(values)


    # ------------------------ PRIVATE MAIN METHODS ---------------------------


    @api.multi
    def _range(self):
        for record in self:
            start = fields.Date.from_string(record.start)
            final_date = fields.Date.from_string(record.final_date)
            return record.range(
                start,
                record.rrule_type,
                record.interval,
                record.count if record.end_type == 'count' else final_date,
                holidays=None,
                workdays=None
            )


    # -------------------------- AUXILIARY METHODS ----------------------------


    @api.model
    def _utc_o_clock(self, offset=0, dateonly=False):
        """ Returns Odoo valid current date or datetime with offset.
        This method will be used to set default values for date/time fields

        @param offset: offset in hours
        @param dateonly: return only date without time
        """
        ctx_now = datetime.now(timezone(self.env.context.get('tz', 'utc')))
        utc_now = ctx_now.astimezone(utc)
        utc_offset = utc_now + timedelta(hours=offset)

        utc_ock = utc_offset.replace(minute=0, second=0, microsecond=0)

        if dateonly == True:
            result = fields.Date.to_string(utc_ock.date())
        else:
            result = fields.Datetime.to_string(utc_ock)

        return result


    @staticmethod
    def _get_duration(start, stop):
        """ Get the duration value between the 2 given dates. This method will
        be used to compute duration field value in all day appointments.
        """

        if start and stop:
            diff = fields.Datetime.from_string(stop) - fields.Datetime.from_string(start)
            if diff:
                duration = float(diff.days) * 24 + (float(diff.seconds) / 3600)
                return round(duration, 2)

            return 0.0

    @staticmethod
    def _date_trunc(dt):
        """ If dt is a date return dt else if dt is a datetime returns dt.date()
        """

        return dt.date() if hasattr(dt, 'date') else dt


    # --------------------------- PUBLIC METHODS ------------------------------


    @staticmethod
    def _normalize_holidays(holidays):
        """ Transforms a given single value or None in a list and returns it
        """

        # STEP 1: Check if value is None (default) and convert it to an empty list
        holidays = holidays or []

        # STEP 2: Check if values is an unique value and convert it to a list
        if isinstance(holidays, date) or isinstance(holidays, datetime):
            holidays = [holidays]

        # STEP 3: Ensure all values are date and not datetimes
        return [dt.date() if isinstance(dt, datetime) else dt for dt in holidays]

    @staticmethod
    def _normalize_workdays(workdays):
        """ If a single value is given this method transforms it in a list,
        otherwise if the given value is None it sets workdays to the default
        list with the positions from monday to friday.
        """

        if workdays == None:
            workdays = [1, 2, 3, 4, 5]
        elif not hasattr(workdays, '__iter__'):
            workdays = [workdays]

        return workdays


    @staticmethod
    def _get_limits(end_value):
        if isinstance(end_value, int):
            return date.max, end_value
        else:
            return (
                end_value.date() if isinstance(end_value, datetime) else end_value,
                maxint
            )

    @staticmethod
    def _in_range_and_not_holiday(start, final_date, holidays):
        """ Checks if is not the given date equal to None, it's less or equal to
        final_date, it's not in holidays and (optionallly) if is it a workdays
        """

        return start <= final_date and start not in holidays

    @staticmethod
    def _workdays_of_the_week(start, workdays=None, relative=False):
        workday_list = []

        # STEP 3: Workdays must be a list. If the list is not given, default
        # will be used instead
        if workdays == None:
            workdays = [1, 2, 3, 4, 5]
        elif not hasattr(workdays, '__iter__'):
            workdays = [workdays]

        # STEP 2: if relative was set to False monday will be use as first day
        start = start if relative else start - timedelta(start.weekday())

        # STEP 3: Append all days in week
        for x in range(0, 8 - start.isoweekday()):
            new_wd = start + timedelta(days=x)
            if new_wd.isoweekday() in workdays:
                workday_list.append(new_wd)

        return workday_list


    @staticmethod
    def _next_daily_date(start, offset, interval, reserved=None):
        #pylint: disable=I0011,W0613

        return start + timedelta(days=interval * offset)


    @classmethod
    def _next_weekly_date(cls, start, offset, interval, workdays):
        #pylint: disable=I0011,W0613
        next_day = start + timedelta(1)
        w1 = cls._workdays_of_the_week(next_day, workdays, relative=True)
        len_w1 = len(w1)

        offset = (offset * interval)

        if len_w1 and offset <= len_w1:
            result = w1[offset-1]
        else:
            monday = start + timedelta(8 - start.isoweekday())
            offset = offset - len_w1 - 1

            weeks = int(offset/len(workdays))
            day_index = int(offset%len(workdays))

            target_date = monday + timedelta(weeks=weeks)
            target_week = cls._workdays_of_the_week(target_date, workdays, relative=False)

            result = target_week[day_index]

        return result


    @staticmethod
    def _next_monthly_date(start, offset, interval, reserved=None):
        #pylint: disable=I0011,W0613

        # STEP 1: Compute all months from start date
        total_months = start.month + (interval * offset)

        # STEP 2: Compute years, remaining months in the last year and a safe_day
        # safe_day allows to move from a short month (28, 29, 30) to a longer one (31)
        var_y = start.year + int((total_months - 1) / 12)
        var_ym = int(total_months % 12) or 12
        safe_day = min(start.day, 28)

        # STEP 3: Computes new safe date moving the pointer to the a safe day
        # in the next month
        safe_date = start.replace(year=var_y, month=var_ym, day=safe_day)

        # STEP 3:
        if start.day > 28:
            ld = monthrange(safe_date.year, safe_date.month)
            new_date = safe_date.replace(day=min(ld[1], start.day))
        else:
            new_date = safe_date

        # STEP 4: Returns the new_day
        return new_date


    @staticmethod
    def _next_yearly_date(start, offset, interval, reserved=None):
        #pylint: disable=I0011,W0613

        var_y = start.year + interval * offset
        safe_day = min(start.day, 28)

        safe_date = start.replace(year=var_y, day=safe_day)

        if start.day > 28:
            ld = monthrange(safe_date.year, safe_date.month)
            new_date = safe_date.replace(day=min(ld[1], start.day))
        else:
            new_date = safe_date

        return new_date


    @classmethod
    def _range_get_specific_next_method(cls, rrule_type):
        """ Gets the specific required method to compute next date and the
        optional method to adjust date, both for given `rrule_type`.
        """

        next_date_method = getattr(cls, u'_next_{}_date'.format(rrule_type))

        return next_date_method


    @classmethod
    def range(cls, start, rrule_type, interval, end_value, holidays=None, workdays=None):
        """ Computes all dates from `start` (date) to end_value (int or date) using
        given rrule_type and interval.

        @param start: the date will be used as the beginning
        @param rrule_type (str): daily, weekly, monthly or yearly
        @interval (int): Number of periods from one date to the next one
        @end_value (int or date): the last date or the number of items in range
        @holidays (list or date): List of dates that will never be added to the list
        @workdays (list): list of ISO week days  will be considered as workdays

        @note: given datetime (type) will be truncated to date (type) values
        @note: end_value must be greater than zero or later than start date,
        otherwise method returns an empty list
        @note: workdays will be used only with 'weekly' rrule_type
        @note: default holidays are empty
        @note: defaul workdays are from Monday to Friday (both included)
        """

        result = []

        # STEP 1: Ensure bounds are dates and not datetimes
        start = cls._date_trunc(start)

        # STEP 2: Limit can be a future date or number (integer) of dates
        # This sets the unused, between both variables, to the maximum value
        final_date, count = cls._get_limits(end_value)
        if count == 0 or start > final_date:
            return result # EARLY METHOD EXIT

        # STEP 3: check if all the given parameteres are compatible with each other
        assert interval > 0 or count == 1 or start == final_date, \
            u'The given parameters are incompatible with each other. ' + \
            u'Interval with Zero as value will return a single date or nothing'

        # STEP 4: Converts date, datetime and None values in a list
        holidays = cls._normalize_holidays(holidays)

        # STEP 5.b: Workdays must be a list. If the list is not given, default
        # will be used instead
        workdays = cls._normalize_workdays(workdays)

        # STEP 6: Prevent nevative intervals
        interval = max(0, interval)

        # STEP 7: Stores given start date if is valid
        # result = [start] if start <= final_date and  and count > 0 else []
        if start and \
           (rrule_type != 'weekly' or start.isoweekday() in workdays) and \
           cls._in_range_and_not_holiday(start, final_date, holidays):
            result.append(start)

        # STEP 8: If interval is 0 the method has finished
        if interval <= 0:
            return result # EARLY METHOD EXIT

        # STEP 8: Prepair loop: offset, initial date and method to move forward
        offset = 1
        specific_next_method = cls._range_get_specific_next_method(rrule_type)
        # new_date = specific_next_method(start, offset, interval, workdays)
        new_date = start

        # STEP 9: Performs a loop getting valid days from start to final_date or count
        while new_date < final_date and len(result) < count:

            # STEP 9.a: Call specific method to move forward one unit
            new_date = specific_next_method(start, offset, interval, workdays)

            # STEP 9.b: Check if current (ensured) date is not in holidays and
            # add it to the results list
            if cls._in_range_and_not_holiday(new_date, final_date, holidays):
                result.append(new_date)

            offset = offset + 1

            ### KILL SWITCH - Prevents an eventual code error in loop locks the server ###
            if offset >= cls._kill_switch:
                _logger.error(
                    (u'A KILL SWITCH WAS ACTIVATED on %s->range at %d loop # '
                     u'new_date: %s, final_date: %s, len(result): %d, count: %d'),
                    cls._name, offset, new_date, final_date, len(result), count
                )
                break

        # STEP 10: Return the list of valid dates
        return result


    @classmethod
    def EDate(cls, dt, months):
        """ Returns the serial number of the date before or after a specified
        number of months

        @note: works like Excel function EDate
        """

        dt = cls._date_trunc(dt)

        return dt + timedelta(months=months)


    @classmethod
    def WorkDay(cls, dt, days, work_days=None, holidays=None):
        """ Returns the serial number of the date before or after a specified
        number of workdays with custom work week parameter

        @note: works like Excel function WorkDayIntl
        @note: work_days parameter uses iso format (monday = 1, ..., sunday = 7)
        """

        dt = cls._date_trunc(dt)

        if days != 0:

            # STEP 1: Set default workdays (monday, ... to ... ,friday)
            if work_days == None:
                work_days = [1, 2, 3, 4, 5]

            # STEP 2: Converts date, datetime and None values in a list
            holidays = cls._normalize_holidays(holidays)

            # STEP 3: Compute if count will increase or decrease
            inc = int(days / abs(days))
            days = abs(days)

            # STEP 4: Go to the first (Forward or backward) workday and decrease counter
            if dt.isoweekday() not in work_days or dt in holidays:
                days = days - 1
                while dt.isoweekday() not in work_days or dt in holidays:
                    dt = dt + timedelta(days=inc)

            # STEP 5: Loop until the last workday decreasing counter
            while days > 0:
                dt = dt + timedelta(days=inc)
                if dt.isoweekday() in work_days and dt not in holidays:
                    days = days - 1

        return dt

    @classmethod
    def WorkDays(cls, dt1, dt2, work_days=None, holidays=None):
        """ Computes workdays beetween two given dates

        @note: works like Excel function NetworkDays.Intl
        @note: work_days parameter uses iso format (monday = 1, ..., sunday = 7)
        """

        # STEP 1: Trunc datetimes to date
        dt1 = cls._date_trunc(dt1)
        dt2 = cls._date_trunc(dt2)

        # STEP 2: Compute difference, in CALENDAR days, beetween given dates
        # Difference will be a absolute value, the sign will be stored in inc varriable
        result = abs((dt2 - dt1).days)
        inc = -1 if dt1 > dt2 else 1

        # STEP 3: Set default workdays (monday, ... to ... ,friday)
        if work_days == None:
            work_days = [1, 2, 3, 4, 5]

        # STEP 4: Converts date, datetime and None values in a list
        holidays = cls._normalize_holidays(holidays)

        if result != 0:

            # STEP 5: Loop until the last day and decreasing counter for each
            # nonworking day
            while dt1 != dt2:
                if dt1.isoweekday() not in work_days or  dt1 in holidays:
                    result = result - 1
                dt1 = dt1 + timedelta(inc)

        # STEP 6: Adjust counter computing the last date
        if dt2.isoweekday() in work_days and dt2 not in holidays:
            result = result + 1

        return int(result * inc)
