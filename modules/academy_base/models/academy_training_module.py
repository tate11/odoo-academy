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


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)


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

    training_unit_ids = fields.One2many(
        string='Training units',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Training units in this module',
        comodel_name='academy.training.unit',
        inverse_name='training_module_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
        oldname='training_unit_ids'
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

    training_unit_count = fields.Integer(
        string='Units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Number of training units in module',
        compute='_compute_training_unit_count',
    )


    # ----------------- AUXILIARY FIELD METHODS AND EVENTS --------------------


    @api.multi
    @api.depends('training_unit_ids', 'ownhours')
    def _compute_hours(self):
        for record in self:
            if record.training_unit_ids:
                record.hours = sum(record.training_unit_ids.mapped('hours'))
            else:
                record.hours = record.ownhours

    @api.multi
    @api.depends('training_unit_ids')
    def _compute_training_unit_count(self):
        for record in self:
            record.training_unit_count = len(record.training_unit_ids)


