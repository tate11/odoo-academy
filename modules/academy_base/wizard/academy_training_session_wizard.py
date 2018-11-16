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



    start_datetime = fields.Datetime(
        string='Start',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help='Start date and time'
    )

    start_date = fields.Date(
        string='Start date',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: fields.Date.context_today(self), # pylint: disable=locally-disabled, W0108
        help='Start date'
    )

    stop_date = fields.Date(
        string='Stop date',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: fields.Date.context_today(self), # pylint: disable=locally-disabled, W0108
        help='End date'
    )

    duration = fields.Float(
        string='Duration',
        required=False,
        readonly=False,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Duration'
    )

    allday = fields.Boolean(
        string='Allday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='All day'
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
        required=False,
        readonly=False,
        index=False,
        default=False,
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
        required=False,
        readonly=False,
        index=False,
        default=False,
        help=False,
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
        default=False,
        help='Monday'
    )

    tu = fields.Boolean(
        string='Tuesday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Tuesday'
    )

    we = fields.Boolean(
        string='Wednesday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Wednesday'
    )

    th = fields.Boolean(
        string='Thursday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Thursday'
    )

    fr = fields.Boolean(
        string='Friday',
        required=False,
        readonly=False,
        index=False,
        default=False,
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
        required=False,
        readonly=False,
        index=False,
        default=False,
        help=False,
        selection= [
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
        string='By day',
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

    final_date = fields.Date(
        string='Repeat until',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: fields.Date.context_today(self), # pylint: disable=locally-disabled, W0108
        help=False
    )
