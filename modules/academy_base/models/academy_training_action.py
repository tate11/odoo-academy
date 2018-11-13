# -*- coding: utf-8 -*-
""" AcademyTrainingAction

This module contains the academy.training.action Odoo model which stores
all training action attributes and behavior.

"""


from logging import getLogger

from datetime import datetime, timedelta
from pytz import timezone, utc

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.exceptions import ValidationError

from . import custom_model_fields


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTrainingAction(models.Model):
    """ Each of the creditable qualifications in catalog.

    Fields:
      action_name (Char): Human readable name which will identify each record.

    """


    _name = 'academy.training.action'
    _description = u'Academy training action'

    _rec_name = 'action_name'
    _order = 'action_name ASC'

    # 'appointment.manager',
    _inherit = ['academy.abstract.image', 'mail.thread', 'academy.abstract.observable']

    _inherits = {'academy.training.activity': 'training_activity_id'}

    action_name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Enter new name',
        size=100,
        translate=True,
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

    # pylint: disable=locally-disabled, w0212
    start = fields.Datetime(
        string='Start',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self._utc_o_clock(),
        help='Start date of an event, without time for full days events'
    )

    # pylint: disable=locally-disabled, w0212
    end = fields.Datetime(
        string='End',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self._utc_o_clock(),
        help='Stop date of an event, without time for full days events',
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
        relation='academy_training_action_knowledge_area_rel',
        column1='training_action_id',
        column2='knowledge_area_id',
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
        relation='academy_training_action_training_modality_rel',
        column1='training_action_id',
        column2='training_modality_id',
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
        relation='academy_training_action_training_methodology_rel',
        column1='training_action_id',
        column2='training_methodology_id',
        domain=[],
        context={},
        limit=None
    )

    training_activity_id = fields.Many2one(
        string='Training activity',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Training activity will be imparted in this action',
        comodel_name='academy.training.activity',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    action_code = fields.Char(
        string='Internal code',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Enter new internal code',
        size=12,
        translate=False
    )

    seating = fields.Integer(
        string='Seating',
        required=False,
        readonly=False,
        index=False,
        default=20,
        help='Maximum number of sign ups allowed'
    )

    training_action_enrolment_ids = fields.One2many(
        string='Enrolments',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.action.enrolment',
        inverse_name='training_action_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )


    training_resource_ids = custom_model_fields.Many2ManyThroughView(
        string='Training resources',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Choose related resources',
        comodel_name='academy.training.resource',
        relation='academy_training_action_training_resource_rel',
        column1='training_action_id',   # this is the name in the SQL VIEW
        column2='training_resource_id', # this is the name in the SQL VIEW
        domain=[],
        context={},
        limit=None,
    )


    # ------------------------------ CONSTRAINS -------------------------------


    @api.constrains('end')
    def _check_end(self):
        """ Ensures end field value is greater then start value """
        for record in self:
            if record.end <= record.start:
                raise ValidationError("End date must be greater then start date")


    # -------------------------- OVERLOADED METHODS ---------------------------

    @api.one
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        """ Prevents new record of the inherited (_inherits) model will be
        created
        """

        default = dict(default or {})
        default.update({
            'training_activity_id': self.training_activity_id.id
        })

        rec = super(AcademyTrainingAction, self).copy(default)
        return rec

    # -------------------------- AUXILIARY METHODS ----------------------------

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

        if dateonly is True:
            result = fields.Date.to_string(utc_ock.date())
        else:
            result = fields.Datetime.to_string(utc_ock)

        return result


