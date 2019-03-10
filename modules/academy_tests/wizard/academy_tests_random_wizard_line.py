# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Academy Tests Random Wizard Line

This module contains the academy.tests.random.wizard.line. an unique Odoo model
which contains all Academy Tests Random Wizard Line  attributes and behavior.

This model is the representation of the real life academy tests random wizard line

Classes:
    AcademyTestsRandomWizardLine: This is the unique model class in this module
    and it defines an Odoo model with all its attributes and related behavior.

    Inside this class can be, in order, the following attributes and methods:
    * Object attributes like name, description, inheritance, etc.
    * Entity fields with the full definition
    * Computed fields and required computation methods
    * Events (@api.onchange) and other field required methods like computed
    domain, defaul values, etc.
    * Overloaded object methods, like create, write, copy, etc.
    * Public object methods will be called from outside
    * Private auxiliary methods not related with the model fields, they will
    be called from other class methods


Todo:
    * Complete the model attributes and behavior

"""


from logging import getLogger
from pprint import pprint

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.tools.translate import _


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)


WIZARD_LINE_STATES = [
    ('step1', 'General'),
    ('step2', 'Topics/Categories'),
    ('step3', 'Tests'),
    ('step4', 'Questions')
]

# in question, in this line, exclude/include
FIELD_MAPPING = [
    ('type_id', 'type_ids', 'exclude_types'),
    ('test_ids', 'test_ids', 'exclude_tests'),
    ('topic_id', 'topic_ids', 'exclude_topics'),
    ('category_ids', 'category_ids', 'exclude_categories'),
    ('tag_ids', 'tag_ids', 'exclude_tags'),
    ('level_id', 'level_ids', 'exclude_levels'),
    ('id', 'question_ids', 'exclude_questions'),
]


# pylint: disable=locally-disabled, R0903, W0212
class AcademyTestsRandomWizardLine(models.Model):
    """ This model is the representation of the academy tests random wizard line

    Fields:
      name (Char)       : Human readable name which will identify each record
      description (Text): Something about the record or other information which
      has not an specific defined field to store it.
      active (Boolean)  : Checked do the record will be found by search and
      browse model methods, unchecked hides the record.

    """


    _name = 'academy.tests.random.wizard.line'
    _description = u'Academy Tests Random Wizard Line'


    _rec_name = 'name'
    _order = 'name ASC'


    state = fields.Selection(
        string='State',
        required=True,
        readonly=False,
        index=False,
        default='step1',
        help=False,
        selection=WIZARD_LINE_STATES
    )

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help="Name for this line",
        size=255,
        translate=True,
        track_visibility='onchange'
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Something about this line',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help=('If the active field is  to false, it will allow you to '
              'hide record without removing it')
    )

    random_wizard_id = fields.Many2one(
        string=' ',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.tests.random.wizard.set',
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
        default=20,
        help='Maximum number of questions can be append'
    )

    type_ids = fields.Many2many(
        string='Types',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.tests.question.type',
        relation='academy_tests_random_wizard_line_question_type_rel',
        column1='random_wizard_line_id',
        column2='type_id',
        domain=[],
        context={},
        limit=None
    )

    exclude_types = fields.Boolean(
        string='Exclude selected types',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check this to disallow selected records instead allow them'
    )

    disallow_attachments = fields.Boolean(
        string='Disallow all attachments',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check this to exclude all questions have attachments'
    )

    test_ids = fields.Many2many(
        string='Tests',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose allowed tests or leave empty to allow all',
        comodel_name='academy.tests.test',
        relation='academy_tests_random_wizard_line_test_rel',
        column1='random_wizard_line_id',
        column2='test_id',
        domain=[],
        context={},
        limit=None
    )

    exclude_tests = fields.Boolean(
        string='Exclude selected tests',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check this to disallow selected records instead allow them'
    )

    topic_ids = fields.Many2many(
        string='Topics',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose allowed topics or leave empty to allow all',
        comodel_name='academy.tests.topic',
        relation='academy_tests_random_wizard_line_topic_rel',
        column1='random_wizard_line_id',
        column2='topic_id',
        domain=[],
        context={},
        limit=None
    )

    exclude_topics = fields.Boolean(
        string='Exclude selected topics',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check this to disallow selected records instead allow them'
    )

    category_ids = fields.Many2many(
        string='Categories',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose allowed categories or leave empty to allow all',
        comodel_name='academy.tests.category',
        relation='academy_tests_random_wizard_line_category_rel',
        column1='random_wizard_line_id',
        column2='category_id',
        domain=[],
        context={},
        limit=None
    )

    exclude_categories = fields.Boolean(
        string='Exclude selected categories',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check this to disallow selected records instead allow them'
    )

    tag_ids = fields.Many2many(
        string='Labels',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose allowed tags or leave empty to allow all',
        comodel_name='academy.tests.tag',
        relation='academy_tests_random_wizard_line_tag_rel',
        column1='random_wizard_line_id',
        column2='tag_id',
        domain=[],
        context={},
        limit=None
    )

    exclude_tags = fields.Boolean(
        string='Exclude selected tags',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check this to disallow selected records instead allow them'
    )

    level_ids = fields.Many2many(
        string='Levels',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose allowed levels or leave empty to allow all',
        comodel_name='academy.tests.level',
        relation='academy_tests_random_wizard_line_level_rel',
        column1='random_wizard_line_id',
        column2='level_id',
        domain=[],
        context={},
        limit=None
    )

    exclude_levels = fields.Boolean(
        string='Exclude selected levels',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check this to disallow selected records instead allow them'
    )

    question_ids = fields.Many2many(
        string='Questions',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose allowed questions or leave empty to allow all',
        comodel_name='academy.tests.question',
        relation='academy_tests_random_wizard_line_question_rel',
        column1='random_wizard_line_id',
        column2='question_id',
        domain=[],
        context={},
        limit=None
    )

    exclude_questions = fields.Boolean(
        string='Exclude selected questions',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check this to disallow selected records instead allow them'
    )


    # -------------------------- MANAGEMENT FIELDS ----------------------------


    type_count = fields.Integer(
        string='Types',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Show number of types',
        store=False,
        compute='compute_type_count'
    )

    test_count = fields.Integer(
        string='Tests',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Show number of tests',
        store=False,
        compute='compute_test_count'
    )

    topic_count = fields.Integer(
        string='Topics',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Show number of topics',
        store=False,
        compute='compute_topic_count'
    )

    category_count = fields.Integer(
        string='Categories',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Show number of categories',
        store=False,
        compute='compute_category_count'
    )

    tag_count = fields.Integer(
        string='Tags',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Show number of tags',
        store=False,
        compute='compute_tag_count'
    )

    level_count = fields.Integer(
        string='Levels',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Show number of levels',
        store=False,
        compute='compute_level_count'
    )

    question_count = fields.Integer(
        string='Questions',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Show number of questions',
        store=False,
        compute='compute_question_count'
    )


    @api.multi
    @api.depends('type_ids')
    def compute_type_count(self):
        for record in self:
            sign = -1 if record.exclude_types else 1
            record.type_count = len(record.type_ids) * sign

    @api.multi
    @api.depends('test_ids')
    def compute_test_count(self):
        for record in self:
            sign = -1 if record.exclude_tests else 1
            record.test_count = len(record.test_ids) * sign

    @api.multi
    @api.depends('topic_ids')
    def compute_topic_count(self):
        for record in self:
            sign = -1 if record.exclude_topics else 1
            record.topic_count = len(record.topic_ids) * sign

    @api.multi
    @api.depends('category_ids')
    def compute_category_count(self):
        for record in self:
            sign = -1 if record.exclude_categories else 1
            record.category_count = len(record.category_ids) * sign

    @api.multi
    @api.depends('tag_ids')
    def compute_tag_count(self):
        for record in self:
            sign = -1 if record.exclude_tags else 1
            record.tag_count = len(record.tag_ids) * sign

    @api.multi
    @api.depends('level_ids')
    def compute_level_count(self):
        for record in self:
            sign = -1 if record.exclude_levels else 1
            record.level_count = len(record.level_ids) * sign

    @api.multi
    @api.depends('question_ids')
    def compute_question_count(self):
        for record in self:
            sign = -1 if record.exclude_questions else 1
            record.question_count = len(record.question_ids) * sign


    def _reload_on_step1(self):
        """ Builds an action which loads again transient model record using
        'step3' as state
        @note: actually this method is not used
        """
        self.write({'state': 'step1'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'academy.tests.random.wizard.line',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }


    @staticmethod
    def _domain_item(leaf, ids, exclude):

        if ids:
            operator = 'not in' if exclude else 'in'
            return (leaf, operator, ids)

        return None


    @api.multi
    def get_leafs(self):
        """ Search for questions to append
        """

        self.ensure_one()

        leafs = []
        for field_map in FIELD_MAPPING:
            leaf = field_map[0]
            ids = getattr(self, field_map[1]).mapped('id')
            exclude = getattr(self, field_map[2])
            ditem = self._domain_item(leaf, ids, exclude)
            if ditem:
                leafs.append(ditem)

        if self.disallow_attachments:
            leafs.append(('ir_attachment_ids', '=', False))

        return leafs


    @api.multi
    def get_domain(self):
        """ Search for questions to append
        """

        self.ensure_one()

        domain = self.get_leafs()
        if len(domain) > 1:
            domain = ['&'] + domain

        return domain


    @api.multi
    def perform_search(self):
        """ Search for questions to append
        """
        question_obj = self.env['academy.tests.question']

        question = self.env['academy.tests.question']
        for record in self:
            domain = record.get_domain()
            limit = record.quantity

            ctx = {'sort_by_random' : True}
            result = question_obj.with_context(ctx).search(domain, limit=limit)
            print(domain, '\n', result)
            question = question + result

        return question


    def _get_values(self):
        values = {}

        for k, v in self._fields.items():

            if k in models.MAGIC_COLUMNS or k[0] == '_':
                continue

            elif isinstance(v, fields.Many2one):
                value = getattr(self, k)
                values[k] = value.id if value else None

            elif isinstance(v, (fields.One2many, fields.Many2many)):
                value = [obj.id for obj in getattr(self, k)]
                if value:
                    values[k] = [(6, None, value)]
                else:
                    values[k] = [(5, None, None)]

            else:
                values[k] = getattr(self, k)

        return values


    @api.multi
    def copy_to(self, recordset=None):
        """ Copy values from current record to all records in recordset
        """

        self.ensure_one()

        result = self.env[self._name]
        values = self._get_values()

        if not recordset:
            result = self.create(values)
            print('create result {}'.format(result))
        else:
            result = recordset.write(values)
            print('write result {}'.format(result))

        return result

