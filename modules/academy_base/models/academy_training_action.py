#pylint: disable=I0011,W0212,C0111,F0401,C0103,R0903
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this action.                   #
###############################################################################

from openerp import models, fields, api, api
from logging import getLogger


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
        default='Enables/disables the record',
        help=False
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

    progress = fields.Float(
        string='Progress',
        required=True,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Use widget to manage progress status'
    )

    start = fields.Date(
        string='Start',
        required=False,
        readonly=False,
        index=False,
        default=fields.Date.today(),
        help='Choose the start date'
    )

    end = fields.Date(
        string='End',
        required=False,
        readonly=False,
        index=False,
        default=fields.Date.today(),
        help='Choose the start date'
    )

    internal_action_code = fields.Char(
        string='Internal code',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Enter new internal code',
        size=50,
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

    competencyunitcounting = fields.Integer(
        string='Competency units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help="Show number of competency units",
        compute=lambda self: self._compute_competencyunitcounting()
    )

    trainingunitcounting = fields.Integer(
        string='Training units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help="Show number of training units",
        compute=lambda self: self._compute_trainingunitcounting()
    )

    studentcounting = fields.Integer(
        string='Students',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help="Show number of students on this action",
        compute=lambda self: self._compute_studentcounting()
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

    @api.one
    @api.onchange('professional_qualification_id')
    def _onchange_professional_qualification_id(self):
        self._compute_competencyunitcounting()
        self._compute_trainingunitcounting()

    @api.one
    @api.onchange('training_action_sign_up_ids')
    def _onchange_student_ids(self):
        self._compute_studentcounting()




