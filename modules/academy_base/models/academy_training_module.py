#pylint: disable=I0011,W0212,C0111
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyTrainingModule(models.Model):
    """ Coherent block of training associated with each of the competency units.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.module'
    _description = u'Academy training module'

    _rec_name = 'name'
    _order = 'name ASC'

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
        default='Enables/disables the record',
        help=False
    )

    academy_training_unit_ids = fields.One2many(
        string='Training units',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Training units in this module',
        comodel_name='academy.training.unit',
        inverse_name='academy_training_module_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    hours = fields.Float(
        string='Hours',
        required=False,
        readonly=False,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Length in hours',
        compute=lambda self: self._compute_hours()
    )

    ownhours = fields.Float(
        string='Hours',
        required=False,
        readonly=False,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Length in hours'
    )

    @api.multi
    @api.depends('academy_training_unit_ids', 'ownhours')
    def _compute_hours(self):
        for record in self:
            if record.academy_training_unit_ids:
                record.hours = sum(record.academy_training_unit_ids.mapped('hours'))
            else:
                record.hours = record.ownhours

