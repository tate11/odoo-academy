# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Academy Training Module

This module contains the academy.training.module an unique Odoo model
which contains all Academy Training Module attributes and behavior.

This model is the representation of the real life trainint module. This
is based on Spanish Certificate Training.

Classes:
    AcademyTrainingModule: This is the unique model class in this module
    and it defines an Odoo model with all its attributes and related behavior.

    Inside this class can be, in order, the following attributes and methods:
    * Object attributes like name, description, inheritance, etc.
    * Entity fields with the full definition
    * Computed fields and required computation methods
    * Events (@api.onchange) and other field required methods like computed
    domain, defaul values, etc...
    * Overloaded object methods, like create, write, copy, etc.
    * Public object methods will be called from outside
    * Private auxiliary methods not related with the model fields, they will
    be called from other class methods


Todo:
    * Complete the model attributes and behavior

"""


from logging import getLogger

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api

from .custom_model_fields import Many2manyThroughView


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)


INHERITED_RESOURCES_REL = """
    SELECT
        COALESCE(
            atm.training_module_id, atm."id"
        )::INTEGER as training_unit_id,
        atr."id" as training_resource_id
    FROM
        academy_training_module AS atm
    INNER JOIN academy_training_module_training_resource_rel AS rel
        ON atm."id" = rel.training_module_id
    INNER JOIN academy_training_resource AS atr
        ON rel.training_resource_id = atr."id"
    WHERE
        atr.training_resource_id IS NULL;
"""


# pylint: disable=locally-disabled, R0903
class AcademyTrainingModule(models.Model):
    """ Coherent block of training associated with each of the competency units.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.module'
    _description = u'Academy training module'

    _inherit = ['academy.abstract.image', 'mail.thread']

    _rec_name = 'name'
    _order = 'name ASC'


    # ---------------------------- ENTITY FIELDS ------------------------------


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

    training_module_id = fields.Many2one(
        string='Training module',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Parent module',
        comodel_name='academy.training.module',
        domain=[('training_module_id', '=', False)],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    training_unit_ids = fields.One2many(
        string='Training units',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Training units in this module',
        comodel_name='academy.training.module',
        inverse_name='training_module_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    module_code = fields.Char(
        string='Code',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Enter code for training module',
        size=12,
        translate=True,
        old_name='code'
    )

    ownhours = fields.Float(
        string='Hours',
        required=True,
        readonly=False,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Length in hours'
    )

    training_resource_ids = fields.Many2many(
        string='Resources',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.resource',
        relation='academy_training_module_training_resource_rel',
        column1='training_module_id',
        column2='training_resource_id',
        domain=[],
        context={},
        limit=None
    )

    training_unit_resource_ids = Many2manyThroughView(
        string='Inherited resources',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.resource',
        relation='academy_training_unit_training_resource_rel',
        column1='training_unit_id',
        column2='training_resource_id',
        domain=[],
        context={},
        limit=None,
        sql=INHERITED_RESOURCES_REL
    )

    sequence = fields.Integer(
        string='Sequence',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help='Choose the unit order'
    )

    # --------------------------- COMPUTED FIELDS -----------------------------

    hours = fields.Float(
        string='Hours',
        required=False,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Length in hours',
        compute='_compute_hours',
    )

    @api.multi
    @api.depends('training_unit_ids', 'ownhours')
    def _compute_hours(self):
        for record in self:
            if record.training_unit_ids:
                record.hours = sum(record.training_unit_ids.mapped('hours'))
            else:
                record.hours = record.ownhours


    training_unit_count = fields.Integer(
        string='Units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Number of training units in module',
        compute='_compute_training_unit_count',
    )


    @api.multi
    @api.depends('training_unit_ids')
    def _compute_training_unit_count(self):
        for record in self:
            record.training_unit_count = len(record.training_unit_ids)

    # ----------------- AUXILIARY FIELD METHODS AND EVENTS --------------------

    @api.model
    def create(self, values):
        """ Updates sequence field after create
        """

        result = super(AcademyTrainingModule, self).create(values)

        return result





