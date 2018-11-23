# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Academy Training Session Wizard Line

This module contains the academy.training.session.wizard.line an unique Odoo model
which contains all Academy Training Session Wizard Line attributes and behavior.

This model is the representation of relation between training units and
session wizard

Classes:
    AcademyTrainingSessionWizardLine: This is the unique model class in this
    moduleand it defines an Odoo model with all its attributes and related
    behavior.

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
from datetime import date, time, datetime

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.exceptions import ValidationError


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTrainingSessionWizardLine(models.TransientModel):
    """ This model is the representation of the academy training session wizard line

    Fields:
      name (Char)       : Human readable name which will identify each record
      description (Text): Something about the record or other information witch
      has not an specific defined field to store it.
      active (Boolean)  : Checked do the record will be found by search and
      browse model methods, unchecked hides the record.

    """


    _name = 'academy.training.session.wizard.line'
    _description = u'Academy Training Session Wizard Line'

    _inherits = {'academy.training.module': 'training_unit_id'}

    _rec_name = 'training_unit_id'
    _order = 'sequence ASC'


    training_unit_id = fields.Many2one(
        string='Training unit',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Related training unit',
        comodel_name='academy.training.module',
        domain=[('id', '=', -1)],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    session_wizard_id = fields.Many2one(
        string='Session wizard',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.session.wizard',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    own_sequence = fields.Integer(
        string='Sequence',
        required=True,
        readonly=False,
        index=False,
        default=1,
        help='Module order in training session line'
    )

    following = fields.Boolean(
        string='Following',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check it if this unit start after previous unit is complete',
        oldname='follow_previous'
    )

    start_date = fields.Date(
        string='Start date',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False
    )

    start_time = fields.Float(
        string='Start time',
        required=False,
        readonly=False,
        index=False,
        default=9.0,
        digits=(16, 2),
        help='Start time '
    )

    duration = fields.Float(
        string='Duration',
        required=True,
        readonly=False,
        index=False,
        default=5.0,
        digits=(16, 2),
        help=False
    )

    incomplete = fields.Selection(
        string='Incomplete',
        required=True,
        readonly=False,
        index=False,
        default='next',
        help=('How the last session will be treated if there '
              'are not enough hours to complete them'),
        selection=[
            ('next', 'Use next'),
            ('void', 'Unoccupied'),
            ('fill', 'Occup')
        ]
    )

    maximum = fields.Float(
        string='Maximum',
        required=True,
        readonly=False,
        index=False,
        default=0,
        digits=(16, 2),
        help='Maximum number of hours will be ocuppied'
    )


    # --------------------------- COMPUTED FIELDS -----------------------------

    imparted = fields.Float(
        string='Imparted',
        required=False,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Number of hours which has been imparted',
        compute=lambda self: self._compute_imparted()   # pylint: disable=locally-disabled, W0212
    )

    @api.multi
    @api.depends('training_unit_id')
    def _compute_imparted(self):
        for record in self:
            # pylint: disable=locally-disabled, W0212
            record.imparted = record._get_imparted_hours()


    # --------------- ONCHANGE EVENTS AND OTHER FIELD METHODS -----------------

    @api.onchange('session_wizard_id')
    def _onchange_training_action_id(self):
        action_set = self.session_wizard_id.training_action_id
        unit_set = action_set.training_unit_ids
        _ids = unit_set.mapped('id') or [-1]

        return {'domain': {'training_unit_id': [('id', 'in', _ids)]}}


    @api.onchange('training_unit_id')
    def _onchange_training_unit_id(self):
        unit_set = self.training_unit_id

        self.maximum = unit_set.hours
        self.imparted = self._get_imparted_hours()


    # -------------------------- AUXILIARY METHODS ----------------------------

    def _get_imparted_hours(self):
        act_id = self.session_wizard_id.training_action_id.id or -1
        uni_id = self.training_unit_id.id or -1

        lesson_domain = [
            '&',
            ('training_action_id', '=', act_id),
            ('training_module_id', '=', uni_id),
        ]
        lesson_obj = self.env['academy.training.lesson']
        lesson_set = lesson_obj.search(lesson_domain, \
            offset=0, limit=None, order=None, count=False)

        return sum(lesson_set.mapped('duration') or [0])


