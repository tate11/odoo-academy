#pylint: disable=I0011,W0212
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AptVacancyPosition(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.public.tendering.vacancy.position'
    _description = u'Vacancy position'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Denomination',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Name for this vacancy position',
        size=50,
        translate=True
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Something about this vacancy position',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=True,
        readonly=False,
        index=False,
        default=True,
        help=('If the active field is set to false, it will allow you '
              'to hide record without removing it.')
    )

    employment_group_id = fields.Many2one(
        string='Group',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_employment_group_id(),
        help='Choose employment group for this vacancy position',
        comodel_name='academy.public.tendering.employment.group',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    exam_type_id = fields.Many2one(
        string='Exam type',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_exam_type_id(),
        help='Choose type of exam for this vacancy position',
        comodel_name='academy.public.tendering.exam.type',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False,
    )

    hiring_type_id = fields.Many2one(
        string='Hiring type',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_hiring_type_id(),
        help='Choose hiring type for this vacancy position',
        comodel_name='academy.public.tendering.hiring.type',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False,
    )

    general_public_access = fields.Integer(
        string='Public',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help='Number of vacancy will be offered for new employees'
    )

    general_internal_promotion = fields.Integer(
        string='Promotion',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help=('Number of vacancy will be offered for internal promotion to '
              ' current employees')
    )

    disabilities_public_access = fields.Integer(
        string='Disabilities',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help='Number of vacancy will be offered for new employees with disabilities'
    )

    disabilities_internal_promotion = fields.Integer(
        string='Disabilities Promotion',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help=('Number of vacancy will be offered for internal promotion to '
              ' current employees with disabilities')
    )

    academy_public_tendering_process_id = fields.Many2one(
        string='Public tendering',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose academy public tendering to which this vacancy belongs',
        comodel_name='academy.public.tendering.process',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    total_of_vacancies = fields.Integer(
        string='Vacancies',
        required=False,
        readonly=True,
        index=False,
        default=0,
        compute='compute_total_of_vacancies',
        help='Set number of vacancies'
    )

    # ----------------------- AUXILIAR FIELD METHODS --------------------------

    @api.model
    def _default_employment_group_id(self):
        """ Returns the default value for group_id field.
        """

        xid = 'academy_public_tendering.academy_public_tendering_employment_group_c1'
        record = self.env.ref(xid)

        return record.id

    @api.model
    def _default_exam_type_id(self):
        """ Returns the default value for kind_id field.
        """

        xid = 'academy_public_tendering.academy_public_tendering_exam_type_exam'
        record = self.env.ref(xid)

        return record.id


    @api.model
    def _default_hiring_type_id(self):
        """ Returns the default value for class_id field.
        """

        xid = 'academy_public_tendering.academy_public_tendering_hiring_type_career'
        record = self.env.ref(xid)

        return record

    @api.multi
    @api.depends(
        'general_public_access',
        'general_internal_promotion',
        'disabilities_public_access',
        'disabilities_internal_promotion')
    def compute_total_of_vacancies(self):
        """ Returns computed value for total_of_vacancies field
        """
        for record in self:
            aggregate = record.general_public_access
            aggregate = aggregate + record.general_internal_promotion
            aggregate = aggregate + record.disabilities_public_access
            aggregate = aggregate + record.disabilities_internal_promotion
            record.total_of_vacancies = aggregate

    # --------------------------- ONCHANGE EVENTS -----------------------------

    # @api.one
    @api.onchange('general_public_access')
    def _onchange_general_public(self):
        """ Onchange event for general_public_access field
        """

        self.compute_total_of_vacancies()


    # @api.one
    @api.onchange('general_internal_promotion')
    def _onchange_general_internal(self):
        """ Onchange event for general_internal_promotion field
        """

        self.compute_total_of_vacancies()


    # @api.one
    @api.onchange('disabilities_public_access')
    def _onchange_disabilities_public(self):
        """ Onchange event for disabilities_public_access field
        """

        self.compute_total_of_vacancies()


    # @api.one
    @api.onchange('disabilities_internal_promotion')
    def _onchange_disabilities_internal(self):
        """ Onchange event for disabilities_internal_promotion field
        """

        self.compute_total_of_vacancies()


