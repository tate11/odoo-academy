# -*- coding: utf-8 -*-
""" AcademyTrainingAction

This module contains the academy.action.enrolment Odoo model which stores
all training action attributes and behavior.

"""

from logging import getLogger

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)


# pylint: disable=locally-disabled, R0903
class AcademyTrainingActionEnrolment(models.Model):
    """ This model stores attributes and behavior relative to the
    enrollment of students in academy training actions
    """

    _name = 'academy.training.action.enrolment'
    _description = u'Academy action enrolment'

    _rec_name = 'name'
    _order = 'name ASC'

    _inherits = {
        'res.partner': 'res_partner_id',
        'academy.training.action': 'training_action_id'
    }

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Enter new name',
        size=100,
        translate=True
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Enter new description',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Enables/disables the record'
    )

    res_partner_id = fields.Many2one(
        string='Student',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Choose enroled student',
        comodel_name='res.partner',
        domain=[('is_student', '=', True)],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    training_action_id = fields.Many2one(
        string='Training action',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Choose training action in which the student will be enroled',
        comodel_name='academy.training.action',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    # pylint: disable=locally-disabled, W0212
    training_module_ids = fields.Many2many(
        string='Training modules',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose modules in which the student will be enroled',
        comodel_name='academy.training.module',
        relation='academy_action_enrolment_training_module_rel',
        column1='action_enrolment_id',
        column2='training_module_id',
        domain=[('id', '=', -1)],   # later will be dinamically updated
        context={},
        limit=None
    )


    @api.multi
    @api.onchange('training_action_id')
    def _onchange_training_action_id(self):
        action_set = self.training_action_id
        activity_set = action_set.mapped('training_activity_id')
        competency_set = activity_set.mapped('competency_unit_ids')
        module_set = competency_set.mapped('training_module_id')
        ids = module_set.ids

        self.training_module_ids = module_set

        if module_set:
            domain = {'training_module_ids':  [('id', 'in', ids)]}
            print(domain)
            return {'domain': domain}

        return {'domain': {'training_module_ids':  [('id', '=', -1)]}}
