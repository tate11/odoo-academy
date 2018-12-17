# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0212,E0611,C0103,R0903,C0111,F0401
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from __future__ import division

from openerp import models, fields, api, api
from openerp.tools.translate import _
from openerp.exceptions import ValidationError
from logging import getLogger
from re import search

_logger = getLogger(__name__)


class AcademyQuestion(models.Model):
    """ Questions are the academy tests cornerstone. Each one of the questions
    belongs to a single topic but they can belong to more than one question in
    the selected topic.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.test.question'
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

    academy_test_topic_id = fields.Many2one(
        string='Topic',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Topic to which this question belongs',
        comodel_name='academy.test.topic',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False,
        track_visibility='onchange',
    )

    academy_test_category_ids = fields.Many2many(
        string='Categories',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Categories relating to this question',
        comodel_name='academy.test.category',
        #relation='model_name_this_model_rel',
        #column1='model_name_id}',
        #column2='this_model_id',
        domain=lambda self: self._compute_academy_test_category_ids_domain(),
        context={},
        limit=None,
        track_visibility='onchange'
    )

    academy_test_answer_ids = fields.One2many(
        string='Answers',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Answers will be shown as choice options for this question',
        comodel_name='academy.test.answer',
        inverse_name='academy_test_question_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
        track_visibility='onchange',
    )

    academy_tag_ids = fields.Many2many(
        string='Tags',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Tag can be used to better describe this question',
        comodel_name='academy.test.tag',
        # relation='model_name_this_model_rel',
        # column1='model_name_id}',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None,
        track_visibility='onchange'
    )

    academy_level_id = fields.Many2one(
        string='Difficulty level',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self._default_academy_level_id(),
        help='Difficulty level of this question',
        comodel_name='academy.test.level',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False,
        track_visibility='onchange'
    )

    ir_attachment_ids = fields.Many2many(
        string='Attachments',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Attachments needed to solve this question',
        comodel_name='ir.attachment',
        # relation='ir_attachment_this_model_rel',
        # column1='ir_attachment_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None
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
    )

    academy_test_ids = fields.One2many(
        string='Used in',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Test in witch this question has been used',
        comodel_name='academy.test.test.question.rel',
        inverse_name='academy_test_question_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
        oldname='academy_test_academy_test_question_ids'
    )


    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    def _compute_academy_test_category_ids_domain(self):
        """ Computes domain for academy_test_category_ids, this should allow categories
        only in the selected topic.
        """

        id_list = self.academy_test_topic_id.academy_test_category_ids.mapped('id')

        return [('id', 'in', tuple(id_list))]


    def _default_academy_level_id(self):
        """ Computes the level_id default value
        """

        # STEP 1: Set default to none
        level_id = None

        # STEP 2: Search for all levels sorted by sequence
        academy_level_domain = []
        academy_level_obj = self.env['academy.test.level']
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

    @api.onchange('academy_test_topic_id')
    def _onchange_academy_topid_id(self):
        """ Updates domain form academy_test_category_ids, this shoud allow categories
        only in the selected topic.
        """
        domain = self._compute_academy_test_category_ids_domain()
        _logger.debug(domain)
        return {
            'domain': {
                'academy_test_category_ids': domain
            }
        }


    @api.onchange('ir_attachment_ids')
    def _onchange_ir_attachment_id(self):
        self._compute_ir_attachment_image_ids()


    # -------------------------- PYTHON CONSTRAINS ----------------------------

    @api.constrains('academy_test_answer_ids')
    def _check_academy_test_answer_ids(self):
        """ Check if question have at last one valid answer
        """

        message = _(u'You must specify at least one correct answer')
        if not True in self.academy_test_answer_ids.mapped('is_correct'):
            raise ValidationError(message)




    academy_test_ids = fields.One2many(
        string='Tests',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.test.test.question.rel',
        inverse_name='academy_test_question_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )
