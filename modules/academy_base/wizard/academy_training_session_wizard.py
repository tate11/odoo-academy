# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyTrainingSessionWizard(models.TransientModel):
    """ Wizard to create new session related with a training action

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.session.wizard'
    _description = u'Academy training session wizard'

    _inherits = {'academy.training.action': 'academy_training_action_id'}

    _rec_name = 'academy_training_action_id'
    _order = 'academy_training_action_id ASC'


    academy_training_action_id = fields.Many2one(
        string='Training action',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.action',
        domain=[],
        context={},
        ondelete='cascade',
        # auto_join=False
    )

    action_unit_control_ids = fields.Many2many(
        string='Unit control',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.action.unit.control',
        relation='academy_training_action_unit_control_wizard_rel',
        # column1='model_name_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None,
        compute='_compute_control_ids'
    )

    training_unit_ids = fields.Many2many(
        string='Training units',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Selected training units',
        comodel_name='academy.training.unit',
        # relation='model_name_this_model_rel',
        # column1='model_name_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=5,
        compute='_compute_itemisation_ids'
    )


    @api.multi
    @api.depends('academy_training_action_id')
    def _compute_control_ids(self):
        """ Computes related training action unit control records
        """

        unit_control_obj = self.env['academy.training.action.unit.control']

        for record in self:
            action_id = record.academy_training_action_id.mapped('id')[0]
            unit_control_domain = [
                ('academy_training_action_id', '=', action_id),
                ('remaining', '>', 0)
            ]
            unit_control_set = unit_control_obj.search(unit_control_domain)

            control_ids = [(4, item.mapped('id')[0]) for item in unit_control_set]

            record.action_unit_control_ids = control_ids

    @api.multi
    def _default_control_ids(self):
        """ Computes default values for control_ids field """

        self.ensure_one()

        unit_control_obj = self.env['academy.training.action.unit.control']

        action_id = self.academy_training_action_id.mapped('id')[0]
        unit_control_domain = [
            ('academy_training_action_id', '=', action_id),
            ('remaining', '>', 0)
        ]
        unit_control_set = unit_control_obj.search(unit_control_domain)

        return [(4, item.mapped('id')[0]) for item in unit_control_set]



    @api.multi
    @api.depends('academy_training_action_id')
    def _compute_training_unit_ids(self):
        """ Removes all selected training units when action is changed
        """
        for record in self:
            record.training_unit_ids = [(5)]

    @api.multi
    def append_unit(self, arg):
        print arg

    @api.multi
    def _unit_control_selector_rpc(self, command, args=None):
        """ It provides a means of communication between javascript widget
            ``AcademyTrainingActionUnitControlSelector`` and python model.
        """

        args = args or {}

        print command

        return self, args


