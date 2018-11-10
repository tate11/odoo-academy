# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyCompetencyUnit(models.Model):
    """ Minimum set of professional skills, capable of recognition and partial
    accreditation.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.competency.unit'
    _description = u'Academy competency unit'

    _rec_name = 'name'
    _order = 'professional_qualification_id ASC, sequence ASC, name ASC'

    _inherits = {'academy.training.module': 'training_module_id'}

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
        help='Choose this competency unit order position'
    )

    training_module_id = fields.Many2one(
        string='Training module',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Training module associated with this competency unit',
        comodel_name='academy.training.module',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False,
        oldname='academy_training_module_id'
    )

    professional_qualification_id = fields.Many2one(
        string='Academy professional qualification',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.professional.qualification',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    # pylint: disable=W0212
    training_unit_count = fields.Integer(
        string='Units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Number of training units in module',
        compute=lambda self: self._compute_training_unit_count()
    )


    @api.multi
    @api.depends('training_module_id')
    def _compute_training_unit_count(self):
        for record in self:
            record.training_unit_count = \
                len(record.training_module_id.training_unit_ids)

