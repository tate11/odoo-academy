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

    _inherit = ['academy.abstract.image', 'mail.thread']

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

    training_module_id = fields.Many2one(
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

    unit_code = fields.Char(
        string='Code',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Enter code for training unit',
        size=12,
        translate=True,
        oldname='code'
    )

    training_resource_ids = fields.Many2many(
        string='Resource',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.resource',
        relation='academy_training_resource_training_unit_rel',
        column1='training_resource_id',
        column2='training_unit_id',
        domain=[],
        context={},
        limit=None,
        oldname='training_resource_ids'
    )

    # pylint: disable=W0212
    training_resource_count = fields.Integer(
        string='Resources',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Numer or related resources',
        compute=lambda self: self._compute_training_resource_count()
    )

    @api.multi
    @api.depends('training_resource_ids')
    def _compute_training_resource_count(self):
        for record in self:
            record.training_resource_count = len(record.training_resource_ids)


