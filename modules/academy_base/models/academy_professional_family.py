# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyProfessionalFamily(models.Model):
    """ Set of qualifications according to criteria of affinity of professional
    competence..

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.professional.family'
    _description = u'Academy professional family'

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

    professional_area_ids = fields.One2many(
        string='Profesional area',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.professional.area',
        inverse_name='professional_family_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )
