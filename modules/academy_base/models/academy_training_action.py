#pylint: disable=I0011,W0212,C0111,F0401,C0103,R0903
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this action.                   #
###############################################################################

from openerp import models, fields, api, api, tools
from logging import getLogger
from openerp.exceptions import ValidationError
from openerp.tools.translate import _
from pytz import timezone, utc
from sys import maxsize as maxint
from calendar import monthrange
from datetime import date, datetime, timedelta
from . import custom_model_fields

_logger = getLogger(__name__)


class AcademyTrainingAction(models.Model):
    """ Each of the creditable qualifications in catalog.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.action'
    _description = u'Academy training action'

    _rec_name = 'name'
    _order = 'name ASC'

    # 'appointment.manager', 
    _inherit = ['academy.image.model', 'mail.thread']

    _inherits = {'academy.professional.qualification': 'professional_qualification_id'}

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

    start = fields.Datetime(
        string='Start',
        required=True,
        readonly=True,
        index=False,
        default=lambda self: self._utc_o_clock(),
        help='Start date of an event, without time for full days events'
    )

    stop = fields.Datetime(
        string='End',
        required=True,
        readonly=True,
        index=False,
        default=lambda self: self._utc_o_clock(),
        help='Stop date of an event, without time for full days events'
    )

    application_scope_id = fields.Many2one(
        string='Application scope',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.application.scope',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    professional_category_id = fields.Many2one(
        string='Professional category',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose related professional category',
        comodel_name='academy.professional.category',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    training_action_category_id = fields.Many2one(
        string='Training action category',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose related training action',
        comodel_name='academy.training.action',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    knowledge_area_ids = fields.Many2many(
        string='Knowledge areas',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose related knowledge areas',
        comodel_name='academy.knowledge.area',
        #relation='academy_knowle_area_this_model_rel',
        #column1='academy_knowle_area_id',
        #column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    training_modality_ids = fields.Many2many(
        string='Training modalities',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose training modalities',
        comodel_name='academy.training.modality',
        #relation='model_name_this_model_rel',
        #column1='model_name_id',
        #column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    training_methodology_ids = fields.Many2many(
        string='Training methodology',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose training methodologies',
        comodel_name='academy.training.methodology',
        #relation='model_name_this_model_rel',
        #column1='model_name_id',
        #column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    professional_qualification_id = fields.Many2one(
        string='Professional qualification',
        required=True,
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

    internal_action_code = fields.Char(
        string='Internal code',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Enter new internal code',
        size=12,
        translate=True
    )

    training_action_sign_up_ids = fields.One2many(
        string='Students',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.action.sign_up',
        inverse_name='academy_training_action_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    seating = fields.Integer(
        string='Seating',
        required=False,
        readonly=False,
        index=False,
        default=20,
        help='Maximum number of sign ups allowed'
    )

    academy_training_resource_ids = custom_model_fields.Many2ManyThroughView(
        string='Training resources',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Choose related resources',
        comodel_name='academy.training.resource',
        relation='academy_training_action_academy_training_resource_rel',
        column1='academy_training_action_id',   # this is the name in the SQL VIEW
        column2='academy_training_resource_id', # this is the name in the SQL VIEW
        domain=[],
        context={},
        limit=None
    )

    competencyunitcounting = fields.Integer(
        string='Competency units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help="Show number of competency units",
        compute='_compute_competencyunitcounting',
    )

    trainingunitcounting = fields.Integer(
        string='Training units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help="Show number of training units",
        compute='_compute_trainingunitcounting',
    )

    studentcounting = fields.Integer(
        string='Students',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help="Show number of students on this action",
        compute='_compute_studentcounting',
    )

    @api.multi
    @api.depends('professional_qualification_id')
    def _compute_competencyunitcounting(self):
        for record in self:
            record.competencyunitcounting = len(
                record.professional_qualification_id.academy_competency_unit_ids)

    @api.multi
    @api.depends('professional_qualification_id')
    def _compute_trainingunitcounting(self):

        for record in self:
            record.trainingunitcounting = len(
                record.professional_qualification_id.academy_competency_unit_ids.mapped(
                    'academy_training_unit_ids'))

    @api.multi
    @api.depends('training_action_sign_up_ids')
    def _compute_studentcounting(self):
        for record in self:
            record.studentcounting = len(record.training_action_sign_up_ids)

    @api.constrains('end')
    def _check_end(self):
        """ Ensures end field value is greater then start value """
        for record in self:
            if record.end <= record.start:
                raise ValidationError("End date must be greater then start date")


    @api.model
    def _utc_o_clock(self, offset=0, dateonly=False):
        """ Returns Odoo valid current date or datetime with offset.
        This method will be used to set default values for date/time fields

        @param offset: offset in hours
        @param dateonly: return only date without time
        """
        ctx = self.env.context
        tz = timezone(ctx.get('tz')) if ctx.get('tz', False) else utc
        ctx_now = datetime.now(tz)
        utc_now = ctx_now.astimezone(utc)
        utc_offset = utc_now + timedelta(hours=offset)

        utc_ock = utc_offset.replace(minute=0, second=0, microsecond=0)

        if dateonly == True:
            result = fields.Date.to_string(utc_ock.date())
        else:
            result = fields.Datetime.to_string(utc_ock)

        return result
