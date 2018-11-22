# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" AcademyTrainingSessionWizard

This module contains the academytrainingsessionwizard an unique Odoo model
which contains all AcademyTrainingSessionWizard attributes and behavior.

This model is a wizard to create all sessions needed for a module

Classes:
    AcademyTrainingSessionWizard: This is the unique model class in this module
    and it defines an Odoo model with all its attributes and related behavior.

    Inside this class can be, in order, the following attributes and methods:
    * Object attributes like name, description, inheritance, etc.
    * Entity fields with the full definition
    * Computed fields and required computation methods
    * Events (@api.onchange) and other field required methods like computed
    domain, defaul values, etc...
    * Overloaded object methods, like create, write, copy, etc.
    * Public object methods will be called from outside
    * Private auxiliary methods not related with the model fields, they will
    be called from other class methods


Todo:
    * Complete the model attributes and behavior

"""


from logging import getLogger
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from sys import maxsize as maxint
import math

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.exceptions import ValidationError


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTrainingSessionWizard(models.TransientModel):
    """ This model is a wizard to create all sessions needed for a module

    Fields:
    """


    _name = 'academy.training.session.wizard'
    _description = u'Academy Training Session Wizard'

    _rec_name = 'id'
    _order = 'id ASC'


    # ---------------------------- ENTITY FIELDS ------------------------------

    training_action_id = fields.Many2one(
        string='Training action',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_training_action_id(), # pylint: disable=locally-disabled, W0212
        help='Choose a training action',
        comodel_name='academy.training.action',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    interval = fields.Integer(
        string='Repeat every',
        required=False,
        readonly=False,
        index=False,
        default=1,
        help='Repeat every (Days/Week/Month/Year)'
    )

    rrule_type = fields.Selection(
        string='Recurrence',
        required=True,
        readonly=False,
        index=False,
        default='weekly',
        help='Let the event automatically repeat at that interval',
        selection=[
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)')
        ]
    )

    end_type = fields.Selection(
        string='End type',
        required=True,
        readonly=False,
        index=False,
        default='count',
        help='End type',
        selection=[
            ('count', 'Number of repetitions'),
            ('end_date', 'End date')
        ]
    )

    count = fields.Integer(
        string='Repeat',
        required=False,
        readonly=False,
        index=False,
        default=1,
        help='Repeat x times'
    )

    mo = fields.Boolean(
        string='Monday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Monday'
    )

    tu = fields.Boolean(
        string='Tuesday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Tuesday'
    )

    we = fields.Boolean(
        string='Wednesday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Wednesday'
    )

    th = fields.Boolean(
        string='Thursday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Thursday'
    )

    fr = fields.Boolean(
        string='Friday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Monday'
    )

    sa = fields.Boolean(
        string='Saturday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Saturday'
    )

    su = fields.Boolean(
        string='Sunday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Sunday'
    )

    month_by = fields.Selection(
        string='Month by',
        required=True,
        readonly=False,
        index=False,
        default='date',
        help='Month by',
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
        help='Date of month'
    )

    week_list = fields.Selection(
        string='Weekday',
        required=True,
        readonly=False,
        index=False,
        default='MO',
        help='Week day',
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
        string='By day',
        required=True,
        readonly=False,
        index=False,
        default='1',
        help='By day',
        selection=[
            ('1', 'First'),
            ('2', 'Second'),
            ('3', 'Third'),
            ('4', 'Fourth'),
            ('5', 'Fifth'),
            ('-1', 'Last')
        ]
    )

    final_date = fields.Date(
        string='Repeat until',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: fields.Date.context_today(self), # pylint: disable=locally-disabled, W0108
        help=False
    )

    state = fields.Selection(
        string='State',
        required=False,
        readonly=False,
        index=False,
        default='step1',
        help='Current wizard state',
        selection=[
            ('step1', 'Training action'),
            ('step2', 'Training modules'),
            ('step3', 'Time interval')
        ]
    )


    # --------------------------- COMPUTED FIELDS -----------------------------

    # IMPORTANT!
    # Following field should be a computed field but instead I have used an
    # @api.onchange (see below) because I need compute field domain at the
    # same time. Even so, the non called compute method is down the field and
    # it's used by the onchange method.
    training_unit_ids = fields.One2many(
        string='Training modules',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.session.wizard.module',
        inverse_name='session_wizard_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
        # compute='_compute_training_unit_ids'
    )

    @api.multi
    @api.depends('training_action_id')
    def _compute_training_unit_ids(self):

        print('Hola')
        for record in self:

            # pylint: disable=locally-disabled, w0212
            unit_set = record._get_units()

            for unit in unit_set:
                record._append_unit_line(unit)


    # ----------------------- REQUIRED FIELD METHODS --------------------------

    def _default_duration(self):    # pylint: disable=locally-disabled, R0201
        hour = time(5, 0, 0)
        hours = datetime.combine(date.min, hour) - datetime.min
        return hours.seconds / 3600.0


    def _default_start_time(self):   # pylint: disable=locally-disabled, R0201
        hour = time(9, 0, 0)
        hours = datetime.combine(date.min, hour) - datetime.min
        return hours.seconds / 3600.0


    def _default_training_action_id(self):
        action_domain = []
        action_obj = self.env['academy.training.action']
        action_set = action_obj.search(action_domain, \
            offset=0, limit=1, order='create_date DESC', count=False)

        return action_set

    # --------------------------- ONCHANGE EVENTS -----------------------------

    @api.onchange('training_action_id')
    def _onchange_training_action_id(self):

        self.training_unit_ids = None

        if self.training_action_id:

            self._compute_training_unit_ids()

            self.state = 'step2'
            domain = [('id', '=', self.training_unit_ids.mapped('id'))]

        else:
            domain = [('id', '=', -1)]
            self.state = 'step1'

        return {
            'domain': {'training_unit_ids': domain}
        }


    @api.onchange('training_unit_ids')
    def _onchange_training_unit_ids(self):
        action_set = self.training_action_id
        module_set = self.training_unit_ids

        if module_set:
            hours = module_set.mapped('duration')
            self.count = int(sum(hours) / 2)
        elif action_set:
            self.state = 'step2'
        else:
            self.state = 'step1'


    @api.onchange('state')
    def _onchange_state(self):
        if not self.training_action_id:
            self.state = 'step1'
        elif not self.training_unit_ids and self.state not in ('step1', 'step2'):
            self.state = 'step2'


    # --------------------------- PUBLIC METHODS ------------------------------

    @api.multi
    def execute(self):
        """ Wizard execute button method """

        #STEP 1: Ensure set has only one record
        self.ensure_one()

        date_list = [date.today()]
        last_date = max(date_list)
        for unit_line in self.training_unit_ids:
            if date_list:
                last_date = max(date_list)
            date_list = self._get_computed_dates_for_module(unit_line, last_date)
            print(date_list)


    # -------------------------- AUXILIARY METHODS ----------------------------


    def _get_units(self):
        """ Get all units in relation action, units will be a final module.
        Some modules have submodules but other have not.
        """

        action_set = self.training_action_id
        compet_set = action_set.mapped('competency_unit_ids')
        module_set = compet_set.mapped('training_module_id')

        unit_set = module_set.filtered(lambda item: not item.training_unit_ids)
        unit_set = unit_set + module_set.mapped('training_unit_ids')

        return unit_set.sorted( \
            key=lambda p: (p.training_module_id.sequence, p.sequence))


    def _append_unit_line(self, unit):
        wizard_model_obj = self.env['academy.training.session.wizard.module']
        sequence = max(self.training_unit_ids.mapped('sequence') or [0]) + 1

        start_date = fields.Date.today() if sequence == 1 else None
        following = False if sequence == 1 else True

        values = {
            'session_wizard_id' : self.id,
            'training_module_id': unit.id,
            'sequence'          : sequence,
            'following'         : following,
            'start_date'        : start_date,
            'start_time'        : 9.0,
            'duration'          : 5.0,
            'maximum'           : unit.ownhours
        }

        self.training_unit_ids = \
            self.training_unit_ids + wizard_model_obj.create(values)

        print(self.training_unit_ids)


    @staticmethod
    def _to_python_date(field_value):
        """ Transforms given field (fields.Date) value to a python date
        """

        return fields.Date.from_string(field_value)


    def _get_bounds(self, module, last_date):
        """ Gets the model: start_date, stop_date and count, next it change
        to the maximum value stop_date or count based on end_type chosen value
        """

        if module.start_date:
            date1 = self._to_python_date(module.start_date)
        else:
            date1 = last_date

        if module.end_type == 'count':
            date2 = date.max
            count = math.ceil(module.maximum / module.duration)
        else:
            date2 = self._to_python_date(module.stop_date)
            count = maxint

        return date1, date2, count


    def _get_time_step(self):
        """ Returns the interval will be used to compute next session date
        """

        num = self.interval

        if self.rrule_type == 'weekly':
            step = relativedelta(weeks=num)
        elif self.rrule_type == 'monthly':
            step = relativedelta(months=num)
        elif self.rrule_type == 'yearly':
            step = relativedelta(years=num)
        else:
            step = relativedelta(days=num)

        return step


    @staticmethod
    def _get_week_dates(date_within_the_week, week_days=False, \
                        mindate=date.min, maxdate=date.max, count=maxint):
        """ Get all dates in the same week as the given date. Optionally,
        you can specify that weekdays will be included.

        @date_within_the_week (date): date within the week
        @week_days (list): week days [0-6](mo-su) will be included
        @mindate         : minimum valid date
        @maxdate         : maximun valid date
        """

        week_days = week_days or [0, 1, 2, 3, 4, 5, 6]

        weekday = date_within_the_week.weekday()
        mo = date_within_the_week - relativedelta(days=weekday)
        su = date_within_the_week + relativedelta(days=6-weekday)

        dates = []
        for ordinal in range(mo.toordinal(), su.toordinal() + 1):
            current = date.fromordinal(ordinal)
            if (mindate <= current <= maxdate) and count > 0:
                if current.weekday() in week_days:
                    dates.append(current)
                    count = count - 1

        return dates


    def _get_weekdays(self):
        """ Returns a zero start numeric list that represents the chosen weekdays
        """
        available = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
        checked = []

        for field in available:
            if getattr(self, field):
                checked.append(available.index(field))

        return checked


    def _get_computed_dates_for_module(self, module, last_date):
        """ Computes all dates based on params given to the wizard.

        @return (list): list with all computed dates
        """

        #STEP 2: Get required values from record
        date1, date2, count = self._get_bounds(module, last_date)
        step = self._get_time_step()
        weekdays = self._get_weekdays()
        rrule_type = self.rrule_type

        #STEP 3: Set up pointer and list
        date_list = []
        current = date1

        #STEP 4: Loop between bounts
        while current <= date2 and count > 0:
            if rrule_type == 'weekly':
                week_dates = self._get_week_dates( \
                    current, weekdays, date1, date2, count)
                date_list.extend(week_dates)

                # Monday of the next week
                current = self._get_week_dates(current + step, [0])[0]
                # Decrease as many days as dates have been added
                count = count - len(week_dates)
            else:
                date_list.append(current)

                current = current + step
                count = count - 1

        #STEP 5: return computed dates
        return date_list



