# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Academy Tests Question Categorize Wizard

This module contains the academy.tests.question.categorize.wizard an unique Odoo model
which contains all Academy Tests Question Categorize Wizard attributes and behavior.

This model is a wizard to allow to categorize selected questions

Classes:
    AcademyTestsQuestionCategorizeWizard: This is the unique model class in this module
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
from odoo.exceptions import ValidationError


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTestsQuestionCategorizeWizard(models.TransientModel):
    """ This model is the representation of the academy tests question categorize wizard
    """


    _name = 'academy.tests.question.categorize.wizard'
    _description = u'Academy Tests Question Categorize Wizard'

    _states = [
        ('step1', 'Targets'),
        ('step2', 'Batch'),
        ('step3', 'Finishing')
    ]

    question_ids = fields.Many2many(
        string='Questions',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_question_ids(),
        help=False,
        comodel_name='academy.tests.question',
        relation='academy_tests_question_categorize_question_rel',
        column1='question_categorize_wizard_id',
        column2='question_id',
        domain=[],
        context={},
        limit=None
    )

    topic_id = fields.Many2one(
        string='Topic',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose topic will be used for all questions',
        comodel_name='academy.tests.topic',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    category_ids = fields.Many2many(
        string='Category',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose categories will be used for all questions',
        comodel_name='academy.tests.category',
        relation='academy_tests_question_categorize_category_rel',
        column1='question_categorize_wizard_id',
        column2='category_id',
        domain=[],
        context={},
        limit=None
    )

    state = fields.Selection(
        string='State',
        required=False,
        readonly=False,
        index=False,
        default='step1',
        help='Current wizard step',
        selection=lambda self: self._states
    )


    # ------------------------------ DEFAULTS ---------------------------------

    def _default_question_ids(self):
        """ It computes default question list loading all has been selected
        before wizard opening
        """

        ids = self.env.context.get('active_ids', [])

        return [(6, None, ids)] if ids else False


    # ------------------------------- EVENTS ----------------------------------

    @api.onchange('topic_id')
    def _onchange_topic_id(self):
        self.category_ids = [(5, None, None)]


    @api.onchange('state')
    def _onchange_state(self):
        valid = self._ensure_state()

        if valid and self.state == self._states[2][0]:
            self.update_targets()

    # --------------------------- PUBLIC METHODS ------------------------------

    @api.multi
    def update_targets(self):
        # pylint: disable=locally-disabled, E1101, C0325
        """ Perform the update
        """

        self.ensure_one()

        topic_id = self.topic_id.id
        category_ids = self.category_ids.mapped('id')

        for question_id in self.question_ids:
            question_id.update({
                'topic_id' : topic_id,
                'category_ids' : [(6, None, category_ids)]
            })


    # -------------------------- AUXILIARY METHODS ----------------------------

    def _ensure_state(self):
        """ Check given step returning it if is valid or the mayor valid step
        otherwise
        """

        valid = [self._states[0][0]]
        result = True

        if self.question_ids:
            valid.append(self._states[1][0])

        if self.topic_id or self.category_ids:
            valid.append(self._states[2][0])

        if self.state not in valid:
            self.state = valid[-1]
            result = False

        return result


    def _reload_on_step3(self):
        """ Builds an action which loads again transient model record using
        'step3' as state
        @note: actually this method is not used
        """
        self.write({'state': 'step3'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'academy.tests.question.categorize.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new'
        }


