# -*- coding: utf-8 -*-
""" AcademyTrainingActivity

This module contains the academy.training.activity Odoo model which stores
all training activity attributes and behavior.

"""


from logging import getLogger

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from . import custom_model_fields


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)


# pylint: disable=locally-disabled, R0903
class AcademyTrainingActivity(models.Model):
    """ This describes the activity offered, its modules, training units
     and available resources.
    """

    _name = 'academy.training.activity'
    _description = u'Academy training activity'

    _rec_name = 'name'
    _order = 'name ASC'

    _inherit = ['academy.abstract.image', 'mail.thread']


    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help=False,
        size=50,
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

    professional_family_id = fields.Many2one(
        string='Professional',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Professional family to whitch this activity belongs',
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
        help='Professional area to whitch this activity belongs',
        comodel_name='academy.professional.area',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    qualification_level_id = fields.Many2one(
        string='Qualification level',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Qualification level to whitch this activity belongs',
        comodel_name='academy.qualification.level',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    activity_code = fields.Char(
        string='Code',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Reference code that identifies the activity',
        size=10,
        translate=True
    )

    general_competence = fields.Text(
        string='General competence',
        required=False,
        readonly=False,
        index=False,
        default='Descrition of general competence that will be acquired at the end of the activity',
        help=False,
        translate=True
    )

    professional_field = fields.Text(
        string='Professional field',
        required=False,
        readonly=False,
        index=False,
        default='Description of the professional field to which this activity is oriented',
        help=False,
        translate=True
    )

    professional_sectors = fields.Text(
        string='Professional sectors',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Description of the professional sector/s to which this activity is oriented',
        translate=True
    )

    # competency_unit_ids = fields.Many2many(
    #     string='Competency units',
    #     required=False,
    #     readonly=False,
    #     index=False,
    #     default=None,
    #     help='Competency units that make up this activity',
    #     comodel_name='academy.competency.unit',
    #     relation='academy_training_activity_competency_unit_rel',
    #     column1='training_activity_id',
    #     column2='competency_unit_id',
    #     domain=[],
    #     context={},
    #     limit=None,
    # )

    competency_unit_ids = fields.One2many(
        string='Competency units',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.competency.unit',
        inverse_name='training_activity_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    training_action_ids = fields.One2many(
        string='Training actions',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Training actions in which this activity is imparted',
        comodel_name='academy.training.action',
        inverse_name='training_activity_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
    )

    # # Many2manyThroughView
    # training_unit_ids = fields.Many2many(
    #     string='Training units',
    #     required=False,
    #     readonly=True,
    #     index=False,
    #     default=None,
    #     help=False,
    #     comodel_name='academy.training.unit',
    #     relation='academy_training_activity_training_unit_rel',
    #     column1='training_activity_id',
    #     column2='training_unit_id',
    #     domain=[],
    #     context={},
    #     limit=None
    # )

    # Many2manyThroughView
    training_resource_ids = fields.Many2many(
        string='Training resources',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.resource',
        relation='academy_training_activity_resource_rel',
        column1='training_activity_id',
        column2='training_resource_id',
        domain=[],
        context={},
        limit=None
    )


    # -------------------------- MANAGEMENT FIELDS ----------------------------

    # pylint: disable=W0212
    competency_unit_count = fields.Integer(
        string='Competency units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help=False,
        compute=lambda self: self._compute_competency_unit_count()
    )

    @api.multi
    @api.depends('competency_unit_ids')
    def _compute_competency_unit_count(self):
        for record in self:
            record.competency_unit_count = len(record.competency_unit_ids)


    # pylint: disable=W0212
    training_action_count = fields.Integer(
        string='Training actions',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help=False,
        store=True,
        compute=lambda self: self._compute_training_action_count()
    )

    @api.multi
    @api.depends('training_action_ids')
    def _compute_training_action_count(self):
        for record in self:
            record.training_action_count = len(record.training_action_ids)


    # # pylint: disable=W0212
    # training_unit_count = fields.Integer(
    #     string='Training units',
    #     required=False,
    #     readonly=True,
    #     index=False,
    #     default=0,
    #     help=False,
    #     compute=lambda self: self._compute_training_unit_count()
    # )

    # @api.multi
    # @api.depends('training_unit_ids')
    # def _compute_training_unit_count(self):
    #     for record in self:
    #         record.training_unit_count = len(record.training_unit_ids)


    # pylint: disable=W0212
    training_resource_count = fields.Integer(
        string='Resources',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help=False,
        compute=lambda self: self._compute_training_resource_count()
    )

    @api.multi
    @api.depends('training_resource_ids')
    def _compute_training_resource_count(self):
        for record in self:
            record.training_resource_count = len(record.training_resource_ids)


    # ---------------------------- PUBLIC FIELDS ------------------------------

    # pylint: disable=locally-disabled, W0613
    @api.multi
    def update_from_external(self, crud, fieldname, recordset):
        """ Observer notify method, will be called by academy.professional.action
        """
        self._compute_training_action_count()
