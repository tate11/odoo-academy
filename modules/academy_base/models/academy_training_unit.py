# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyTrainingUnit(models.Model):
    """ Each of the formative units that make up a module, these are the
    smallest part that can be evaluated.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.unit'
    _description = u'Academy training unit'

    _inherit = ['academy.image.model']

    _rec_name = 'name'
    _order = 'sequence ASC, name ASC'

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

    sequence = fields.Integer(
        string='Sequence',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help="Choose unit order"
    )

    academy_training_module_id = fields.Many2one(
        string='Training module',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Training module to witch this unit belongs',
        comodel_name='academy.training.module',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    hours = fields.Float(
        string='Hours',
        required=False,
        readonly=False,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Length in hours'
    )

    code = fields.Char(
        string='Code',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Enter code for training unit',
        size=12,
        translate=True
    )

    academy_training_resource_ids = fields.Many2many(
        string='Training resource',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.resource',
        # relation='academy_training_resource_this_model_rel',
        # column1='academy_training_resource_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

