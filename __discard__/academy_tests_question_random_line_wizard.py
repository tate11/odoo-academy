# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Academy Tests Question Random Wizard

This module contains the academy.tests.question.random.line.wizard an unique Odoo model
which contains all Academy Tests Append Random Questions attributes and behavior.

This model is the representation of the real life academy tests question random

Classes:
    AcademyTestsAppendRandomQuestions: This is the unique model class in this module
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
from openerp.tools.translate import _

# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTestsQuestionRandomWizardLine(models.TransientModel):
    """ This model is the representation of the academy tests append random questions
    """

    _name = 'academy.tests.question.random.line.wizard'
    _description = u'Academy Question Random Wizard'

    _inherit = ['academy.tests.question.random.line']

    _rec_name = 'id'
    _order = 'name DESC'


    @staticmethod
    def _domain_item(leaf, ids, exclude):

        if ids:
            operator = 'not in' if exclude else 'in'
            return (leaf, operator, ids)

        return None


    def _reload_on_step1(self):
        """ Builds an action which loads again transient model record using
        'step3' as state
        @note: actually this method is not used
        """
        self.write({'state': 'step1'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'academy.tests.question.random.line.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }


    @api.multi
    def process(self):
        """ Search for questions to append
        """
        dfields = [
            ('type_id', 'type_ids', 'exclude_types'),
            ('test_ids', 'test_ids', 'exclude_tests'),
            ('topic_id', 'topic_ids', 'exclude_topics'),
            ('category_ids', 'category_ids', 'exclude_categories'),
            ('tag_ids', 'tag_ids', 'exclude_tags'),
            ('level_id', 'level_ids', 'exclude_levels'),
            ('id', 'question_ids', 'exclude_questions'),
        ]

        domain = []
        for dfield in dfields:
            leaf = dfield[0]
            ids = getattr(self, dfield[1]).mapped('id')
            exclude = getattr(self, dfield[2])
            ditem = self._domain_item(leaf, ids, exclude)
            if ditem:
                domain.append(ditem)

        if self.disallow_attachments:
            domain.append(('ir_attachment_ids', '=', False))

        if len(domain) > 1:
            domain = ['&'] + domain


        question_obj = self.env['academy.tests.question']
        question_set = question_obj.search(domain, limit=self.quantity)

        print(domain, question_set)

        return self._reload_on_step1()















