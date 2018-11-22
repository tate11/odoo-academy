# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Academy Training Session Wizard Module

This module contains the academy.training.session.wizard.module an unique Odoo model
which contains all Academy Training Session Wizard Module attributes and behavior.

This model is the representation of relation between training modules and
session wizard

Classes:
    AcademyTrainingSessionWizardModule: This is the unique model class in this module
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
from datetime import date, time, datetime

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.exceptions import ValidationError


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTrainingSessionWizardModule(models.TransientModel):
    """ This model is the representation of the academy training session wizard module

    Fields:
      name (Char)       : Human readable name which will identify each record
      description (Text): Something about the record or other information witch
      has not an specific defined field to store it.
      active (Boolean)  : Checked do the record will be found by search and
      browse model methods, unchecked hides the record.

    """


    _name = 'academy.training.session.wizard.module'
    _description = u'Academy Training Session Wizard Module'

    _rec_name = 'training_module_id'
    _order = 'sequence ASC'

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

    training_module_id = fields.Many2one(
        string='Training module',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Related training module',
        comodel_name='academy.training.module',
        domain=[('training_module_id', '=', False)],  # pylint: disable=locally-disabled, W0212
        context={},
        ondelete='cascade',
        auto_join=False
    )

    sequence = fields.Integer(
        string='Sequence',
        required=True,
        readonly=False,
        index=False,
        default=1,
        help='Module order in training session line'
    )

    imparted = fields.Float(
        string='Imparted',
        required=False,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Number of hours which has been imparted',
        compute=lambda self: self._compute_imparted() # pylint: disable=locally-disabled, W0212
    )

    @api.multi
    @api.depends('training_module_id', 'session_wizard_id')
    def _compute_imparted(self):
        pass
        # for record in self:
        #     action_id = record.session_wizard_id.training_action_id
        #     session_domain = [
        #         ('training_action_id', '=', action_id.id),
        #         ('training_module_id', '=', record.training_module_id.id)
        #     ]
        #     session_obj = self.env['academy.training.session']
        #     session_set = session_obj.search(session_domain, \
        #         offset=0, limit=None, order=None, count=False)

        #     total = sum(session_set.mapped('hours'))

        #     record.imparted = total


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

    # IMPORTANT: This field is not used yet, in a future can be usefull
    stop_date = fields.Date(
        string='End date',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: fields.Date.context_today(self), # pylint: disable=locally-disabled, W0108
        help=False
    )

    # IMPORTANT: This field is not used yet, in a future can be usefull
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

    maximum = fields.Float(
        string='Maximum',
        required=True,
        readonly=False,
        index=False,
        default=0,
        digits=(16, 2),
        help='Maximum number of hours will be ocuppied'
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
