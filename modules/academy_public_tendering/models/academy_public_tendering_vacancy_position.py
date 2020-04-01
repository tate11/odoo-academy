#pylint: disable=I0011,W0212
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api, api
from odoo.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AptVacancyPosition(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.public.tendering.vacancy.position'
    _description = u'Public tendering, vacancy position'

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
    
    sequence = fields.Integer(
        string='Sequence',
        required=False,
        readonly=False,
        index=False,
        default=1,
        help='Order in which this vacancy position will be displayed in the tender process view'
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help=('If the active field is set to false, it will allow you '
              'to hide record without removing it.')
    )

    employment_group_id = fields.Many2one(
        string='Group',
        required=True,
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
        required=True,
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
        required=True,
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

    academy_public_tendering_vacancy_position_type_id = fields.Many2one(
        string='Vacancy position type',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help=False,
        comodel_name='academy.public.tendering.vacancy.position.type',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    quantity = fields.Integer(
        string='Quantity',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help=False
    )

    academy_public_tendering_process_id = fields.Many2one(
        string='Public tendering',
        required=True,
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


