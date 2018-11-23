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
from calendar import monthrange
import math

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api, _
from openerp.exceptions import UserError


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTrainingSessionWizard(models.TransientModel):
    """ This model is a wizard to create all sessions needed for an unit

    Fields:
    """


    _name = 'academy.training.session.wizard'
    _description = u'Academy Training Session Wizard'

    _rec_name = 'id'
    _order = 'id ASC'


    # ---------------------------- ENTITY FIELDS ------------------------------

    training_action_id = fields.Many2one(
        string='Training action',
        required=True,
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
            ('step2', 'Training units'),
            ('step3', 'Time interval')
        ]
    )

    # --------------------------- COMPUTED FIELDS -----------------------------

    # IMPORTANT!
    # Following fields should be a computed field but instead I have used an
    # @api.onchange (see below) because I need compute field domain at the
    # same time. Even so, the non called compute method is down the field and
    # it's used by the onchange method.

    training_unit_ids = fields.Many2many(
        string='Training units',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.module',
        relation='academy_training_session_wizard_trainining_module_rel',
        column1='session_wizard_id',
        column2='training_unit_id',
        domain=[],
        context={},
        limit=None,
        # compute=lambda self: self._compute_training_unit_ids()
    )

    @api.multi
    @api.depends('training_action_id')
    def _compute_training_unit_ids(self):
        for record in self:
            # pylint: disable=locally-disabled, W0212

            record.training_unit_ids = record._get_units()


    wizard_line_ids = fields.One2many(
        string='Training units',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.session.wizard.line',
        inverse_name='session_wizard_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
        # compute='_compute_wizard_line_ids'
    )

    @api.multi
    @api.depends('training_action_id')
    def _compute_wizard_line_ids(self):

        for record in self:
            # pylint: disable=locally-disabled, w0212
            unit_set = record._get_units() or self.env['academy.training.module']

            unit_lines = []
            index = 1
            for unit in unit_set:
                unit_line = record._append_unit_line(unit, index)
                unit_lines.append(unit_line)
                index = index + 1

            if unit_lines:
                self.wizard_line_ids = unit_lines


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

        self.wizard_line_ids = None

        if self.training_action_id:

            self._compute_training_unit_ids()
            self._compute_wizard_line_ids()

            self.state = 'step2'
            # pylint: disable=locally-disabled, E1101
            domain = [('id', '=', self.wizard_line_ids.mapped('id'))]

        else:
            self.training_unit_ids = self.env['academy.training.module']
            self.wizard_line_ids = self.env['academy.training.session.wizard.line']
            domain = [('id', '=', -1)]
            self.state = 'step1'

        return {
            'domain': {'wizard_line_ids': domain}
        }


    @api.onchange('wizard_line_ids')
    def _onchange_wizard_line_ids(self):
        action_set = self.training_action_id
        unit_set = self.wizard_line_ids

        if unit_set:
            hours = unit_set.mapped('duration')
            self.count = int(sum(hours) / 2)
        elif action_set:
            self.state = 'step2'
        else:
            self.state = 'step1'


    @api.onchange('state')
    def _onchange_state(self):
        if not self.training_action_id:
            self.state = 'step1'
        elif not self.wizard_line_ids and self.state not in ('step1', 'step2'):
            self.state = 'step2'


    # --------------------------- PUBLIC METHODS ------------------------------


    @api.multi
    def execute(self):
        """ Wizard execute button method """

        #STEP 1: Ensure set has only one record
        self.ensure_one()

        line_set = self.wizard_line_ids.sorted(lambda item: item.sequence)

        assert line_set[0].start_date, \
            _('First line start date is required')

        date1 = self._to_python_date(line_set[0].start_date)
        step = self._get_time_step()
        weekdays = self._get_weekdays()
        for line in line_set:
            self._process_line(line, date1, step, weekdays, offset)


    def _process_line(self, line, date1, step, weekdays, offset):
        count = math.ceil((unit.maximum - offset) / unit.duration)


    # -------------------------- AUXILIARY METHODS ----------------------------

    def _get_units(self):
        action_id = self.training_action_id
        activi_id = action_id.training_activity_id
        compet_ids = activi_id.mapped('competency_unit_ids')
        module_ids = compet_ids.mapped('training_module_id')

        unit_set = self.env['academy.training.module']
        for mod_id in module_ids:
            if mod_id.training_unit_ids:
                unit_set = unit_set + mod_id.training_unit_ids
            else:
                unit_set = unit_set + mod_id

        return unit_set.sorted( \
            key=lambda p: (p.training_module_id.sequence, p.sequence))


    def _append_unit_line(self, unit, sequence):
        start_date = fields.Date.today() if sequence == 1 else None
        following = False if sequence == 1 else True

        values = {
            'session_wizard_id' : self.id,
            'training_unit_id'  : unit.id,
            'sequence'          : sequence,
            'following'         : following,
            'start_date'        : start_date,
            'start_time'        : 9.0,
            'duration'          : 5.0,
            'maximum'           : unit.ownhours,
            'incomplete'        : 'next'
        }

        return (0, 0, values)

    @staticmethod
    def _to_python_date(field_value):
        """ Transforms given field (fields.Date) value to a python date
        """

        return fields.Date.from_string(field_value)


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


    def _get_weekdays(self):
        """ Returns a zero start numeric list that represents the chosen weekdays
        """
        available = ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su']
        checked = []

        for field in available:
            if getattr(self, field):
                checked.append(available.index(field))

        return checked


