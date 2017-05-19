# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyProfessionalQualification(models.Model):
    """ Set of qualifications according to criteria of affinity of professional
    competence..

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.professional.qualification'
    _description = u'Academy professional qualification'

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

    # academy_competency_unit_ids = fields.Many2many(
    #     string='Competency units',
    #     required=False,
    #     readonly=False,
    #     index=False,
    #     default=None,
    #     help='Competency units in this training action',
    #     comodel_name='academy.competency.unit',
    #     # relation='academy_competency_unit_this_model_rel',
    #     # column1='academy_competency_unit_id',
    #     # column2='this_model_id',
    #     domain=[],
    #     context={},
    #     limit=None
    # )

    academy_competency_unit_ids = fields.One2many(
        string='Academy competency units',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose related competency units',
        comodel_name='academy.competency.unit',
        inverse_name='professional_qualification_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )


    professional_family_id = fields.Many2one(
        string='Professional family',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose the related professional family',
        comodel_name='academy.professional.family',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    professional_area_id = fields.Many2one(
        string='Professional area',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose the related professional area',
        comodel_name='academy.professional.area',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    internal_code = fields.Char(
        string='Internal code',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Enter new internal code',
        size=50,
        translate=True
    )

    qualification_level_id = fields.Many2one(
        string='Qualification level',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose the related qualification level',
        comodel_name='academy.qualification.level',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )
