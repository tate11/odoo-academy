# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" academy tests

This module contains the academy.tests.question an unique Odoo model
which contains all academy tests attributes and behavior.

This model is the representation of the real life question will be used in
one or more tests

Classes:
    AcademyTest: This is the unique model class in this module
    and it defines an Odoo model with all its attributes and related behavior.

"""


from logging import getLogger

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import ValidationError


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTestsQuestion(models.Model):
    """ Questions are the academy testss cornerstone. Each one of the questions
    belongs to a single topic but they can belong to more than one question in
    the selected topic.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.tests.question'
    _description = u'Referred question'

    _rec_name = 'name'
    _order = 'name ASC'

    _inherit = ['mail.thread']

    # ---------------------------- ENTITY FIELDS ------------------------------

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Text for this question',
        size=1024,
        translate=True,
        track_visibility='onchange'
    )

    preamble = fields.Text(
        string='Preamble',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='What it is said before beginning to question',
        translate=True
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Something about this question',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help=('If the active field is set to false, it will allow you to '
              'hide record without removing it')
    )

    topic_id = fields.Many2one(
        string='Topic',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Topic to which this question belongs',
        comodel_name='academy.tests.topic',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False,
        track_visibility='onchange',
        oldname='academy_topic_id'
    )

    category_ids = fields.Many2many(
        string='Categories',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Categories relating to this question',
        comodel_name='academy.tests.category',
        relation='academy_tests_question_category_rel',
        column1='question_id',
        column2='category_id',
        domain=[],
        context={},
        limit=None,
        track_visibility='onchange',
        oldname='academy_category_ids'
    )

    answer_ids = fields.One2many(
        string='Answers',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Answers will be shown as choice options for this question',
        comodel_name='academy.tests.answer',
        inverse_name='question_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
        track_visibility='onchange',
        oldname='academy_answer_ids'
    )

    tag_ids = fields.Many2many(
        string='Tags',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Tag can be used to better describe this question',
        comodel_name='academy.tests.tag',
        relation='academy_tests_question_tag_rel',
        column1='question_id',
        column2='tag_id',
        domain=[],
        context={},
        limit=None,
        track_visibility='onchange',
        oldname='academy_tag_ids'
    )

    level_id = fields.Many2one(
        string='Difficulty',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self._default_level_id(),
        help='Difficulty level of this question',
        comodel_name='academy.tests.level',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False,
        track_visibility='onchange',
        oldname='academy_level_id'
    )

    ir_attachment_ids = fields.Many2many(
        string='Attachments',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Attachments needed to solve this question',
        comodel_name='ir.attachment',
        relation='academy_tests_question_ir_attachment_rel',
        column1='question_id',
        column2='attachment_id',
        domain=[],
        context={},
        limit=None,
        oldname='academy_ir_attachment_ids'
    )

    ir_attachment_image_ids = fields.Many2many(
        string='Images',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Images needed to solve this question',
        comodel_name='ir.attachment',
        domain=[('index_content', '=', 'image')],
        context={},
        limit=None,
        compute='_compute_ir_attachment_image_ids',
        oldname='academy_ir_attachment_image_ids'
    )

    test_ids = fields.One2many(
        string='Used in',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Test in witch this question has been used',
        comodel_name='academy.tests.test.question.rel',
        inverse_name='question_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
        oldname='academy_test_ids',
    )


    # ----------------------- AUXILIARY FIELD METHODS -------------------------


    def _default_level_id(self):
        """ Computes the level_id default value
        """

        # STEP 1: Set default to none
        level_id = None

        # STEP 2: Search for all levels sorted by sequence
        academy_level_domain = []
        academy_level_obj = self.env['academy.tests.level']
        academy_level_set = academy_level_obj.search(
            academy_level_domain, order="sequence ASC")

        # STEP 3: Gets the middel item from sorted set
        if academy_level_set:
            middle = len(academy_level_set) // 2
            level_id = academy_level_set[middle].id


        return level_id


    @api.multi
    @api.depends('ir_attachment_ids')
    def _compute_ir_attachment_image_ids(self):
        for record in self:
            record.ir_attachment_image_ids = record.ir_attachment_ids.filtered(
                lambda r: r.index_content == u'image')


    # --------------------------- ONCHANGE EVENTS -----------------------------

    @api.onchange('topic_id')
    def _onchange_academy_topid_id(self):
        """ Updates domain form category_ids, this shoud allow categories
        only in the selected topic.
        """
        topic_set = self.topic_id
        valid_ids = topic_set.category_ids & self.category_ids

        self.category_ids = [(6, None, valid_ids.mapped('id'))]


    @api.onchange('ir_attachment_ids')
    def _onchange_ir_attachment_id(self):
        self._compute_ir_attachment_image_ids()


    # -------------------------- PYTHON CONSTRAINS ----------------------------

    @api.constrains('answer_ids', 'name')
    def _check_answer_ids(self):
        """ Check if question have at last one valid answer
        """
        message = _(u'You must specify at least one correct answer')
        if not True in self.answer_ids.mapped('is_correct'):
            raise ValidationError(message)


    test_ids = fields.One2many(
        string='Tests',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.tests.test.question.rel',
        inverse_name='question_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
        oldname='academy_test_ids'
    )


    attachment_count = fields.Integer(
        string='Attachments',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help='Number of attachments',
        compute=lambda self: self._compute_attachment_count()
    )

    @api.multi
    @api.depends('ir_attachment_ids')
    def _compute_attachment_count(self):
        for record in self:
            record.attachment_count = len(record.ir_attachment_ids)


    answer_count = fields.Integer(
        string='Answers',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help='Number of answers',
        compute=lambda self: self._compute_answer_count()
    )

    @api.multi
    @api.depends('answer_ids')
    def _compute_answer_count(self):
        for record in self:
            record.answer_count = len(record.answer_ids)
