#pylint: disable=I0011,W0212,C0111,F0401,C0103,R0903
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this action.                   #
###############################################################################

from openerp import models, fields, api, api, tools
from logging import getLogger
from openerp.exceptions import ValidationError


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
        help='Use widget to manage progress status',
        compute=lambda self: self._compute_progress()
    )

    start = fields.Datetime(
        string='Start',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help='Choose the start date'
    )

    end = fields.Datetime(
        string='End',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
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

    academy_training_session_ids = fields.One2many(
        string='Training sessions',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.session',
        inverse_name='academy_training_action_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
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
        help='Maximun number of sign ups allowed'
    )

    auto_session = fields.Boolean(
        string='Auto create sessions',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check for create sessions automatically'
    )

    session_length = fields.Float(
        string='Session length',
        required=False,
        readonly=False,
        index=False,
        default=1.0,
        digits=(16, 2),
        help='Enter session length in hours'
    )


    interval = fields.Integer(
        string='Repeat Every',
        required=False,
        readonly=False,
        index=False,
        default=1,
        help='Repeat every (Days/Week/Month/Year)'
    )

    rrule_type = fields.Selection(
        string='Recurrency',
        required=False,
        readonly=False,
        index=False,
        default='weekly',
        help='Let the event automatically repeat at that interval',
        selection=[
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('yearly', 'Year(s)'),
        ],
        #states={'done': [('readonly', True)]}
    )

    mo = fields.Boolean(
        string='Monday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for monday"
    )

    tu = fields.Boolean(
        string='Tuesday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for tuesday"
    )

    we = fields.Boolean(
        string='Wednesday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for wednesday"
    )

    th = fields.Boolean(
        string='Thursday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for Thursday"
    )

    fr = fields.Boolean(
        string='Friday',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help="Check for friday"
    )

    sa = fields.Boolean(
        string='Saturday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help="Check for saturday"
    )

    su = fields.Boolean(
        string='Sunday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help="Check for sunday"
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

    sessioncounting = fields.Integer(
        string='Sessions',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help="Show number of sessions on this action",
        compute=lambda self: self._compute_sessioncounting()
    )

    @api.multi
    @api.depends('progress')
    def _compute_progress(self):
        for record in self:
            ses_hours = sum(record.academy_training_session_ids.mapped('hours'))
            act_hours = sum(record.academy_competency_unit_ids.mapped('hours'))
            if act_hours == 0:
                record.progress = 100
            else:
                record.progress = (ses_hours / act_hours) * 100


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

    @api.multi
    @api.depends('academy_training_session_ids')
    def _compute_sessioncounting(self):
        for record in self:
            record.sessioncounting = len(record.academy_training_session_ids)

    # Not needed in Odoo 10
    # @api.one
    # @api.onchange('professional_qualification_id')
    # def _onchange_professional_qualification_id(self):
    #     self._compute_competencyunitcounting()
    #     self._compute_trainingunitcounting()

    # Not needed in Odoo 10
    # @api.onchange('training_action_sign_up_ids')
    # def _onchange_training_action_sign_up_ids(self):
    #     self._compute_studentcounting()


    image = fields.Binary(
        string='Image',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help='This field holds the image used as image for our customers, limited to 1024x1024px.'
    )

    image_medium = fields.Binary(
        string='Image (auto-resized to 128x128)',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help="Medium-sized image of the category. It is automatically " \
             "resized as a 128x128px image, with aspect ratio preserved. " \
             "Use this field in form views or some kanban views.",
        compute="_get_image",
    )

    image_small = fields.Binary(
        string='Image (auto-resized to 64x64)',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help="Small-sized image of the category. It is automatically " \
             "resized as a 64x64px image, with aspect ratio preserved. " \
             "Use this field anywhere a small image is required.",
        compute="_get_image",
    )


    @api.multi
    @api.depends('image')
    def _get_image(self):
        for record in self:
            image = record.image
            if image:
                data = tools.image_get_resized_images(image)
                record.image_medium = data["image_medium"]
                record.image_small = data["image_small"]



    # @api.one
    # @api.onchange('image')
    # def _onchange_image(self):
    #     image = self.image

    #     data = tools.image_get_resized_images(image)
    #     self.image_medium = data["image_medium"]
    #     self.image_small = data["image_small"]

    @api.constrains('end')
    def _check_end(self):
        """ Ensures end field value is greater then start value """
        for record in self:
            if record.end <= record.start:
                raise ValidationError("End date must be greater then start date")



    @api.multi
    def append_session(self):
        pass
