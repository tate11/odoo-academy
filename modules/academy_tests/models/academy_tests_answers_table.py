# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" academy tests

This module contains the academy.tests.answers.table. an unique Odoo model
which contains all academy tests attributes and behavior.

This model uses an SQL view instead an SQL table, therefore it do not store
any data. Each one of the records for this model will represent an entry in
the answers table for a tests, this table is usually attached to the related
test.

Classes:
    AcademyTest: This is the unique model class in this module
    and it defines an Odoo model with all its attributes and related behavior.

"""


from logging import getLogger

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.tools import drop_view_if_exists


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTestsAnswersTable(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.tests.answers.table'
    _description = u'Answers table'

    _rec_name = 'name'
    _order = 'sequence ASC'

    _auto = False

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Letter for this answer',
        size=1024,
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

    academy_test_id = fields.Many2one(
        string='Test',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Test to which this item belongs',
        comodel_name='academy.tests.test',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    academy_question_id = fields.Many2one(
        string='Question',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Question to which this answer belongs',
        comodel_name='academy.tests.question',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    sequence = fields.Integer(
        string='Sequence',
        required=True,
        readonly=False,
        index=False,
        default=10,
        help='Preference order for this question'
    )

    @api.model_cr
    def init(self):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        _sql_query = u"""
            WITH ordered_answers AS (

            -- Ensure answers sequence
                SELECT
                    academy_tests_answer."id",
                    (row_number() OVER (PARTITION BY academy_tests_answer.academy_question_id ORDER BY academy_tests_answer.academy_question_id ASC, academy_tests_answer."sequence", academy_tests_answer."id"))::integer AS "sequence",
                    academy_tests_answer.academy_question_id,
                    academy_tests_answer.is_correct
                FROM academy_tests_answer
                WHERE active = TRUE
                ORDER BY academy_tests_answer.academy_question_id ASC, academy_tests_answer."sequence", academy_tests_answer."id"

            ), ordered_quesions AS (

            -- Ensure questions sequence
                SELECT
                    rel.academy_test_id,
                    rel.academy_question_id,
                    ROW_NUMBER() OVER(PARTITION BY rel.academy_test_id ORDER BY  rel.academy_test_id DESC, rel."sequence" ASC, rel.academy_question_id ASC) as atq_index
                    FROM academy_tests_test_question_rel AS rel
                    WHERE active = TRUE
                ORDER BY rel.academy_test_id DESC, rel."sequence" ASC, rel.academy_question_id ASC

            )

            -- Main query
            SELECT
                ROW_NUMBER() OVER(ORDER BY oq.academy_test_id DESC, oq.atq_index ASC, oq.academy_question_id ASC, oa."sequence" ASC, oa."id" ASC)::INTEGER AS "id",
                oq.academy_test_id::INTEGER,
                oq.academy_question_id::INTEGER,
                oa."id"::INTEGER as academy_tests_answer_id,
                oq.atq_index::INTEGER as "sequence",
                SUBSTRING('ABCDEFGHIJKLMNOPQRSTUVWXYZ' FROM oa."sequence" FOR 1)::VARCHAR AS "name",
                atq."description"::TEXT
            FROM ordered_quesions as oq
            LEFT JOIN (SELECT * FROM ordered_answers WHERE is_correct IS TRUE) as oa on oq.academy_question_id = oa.academy_question_id
            LEFT JOIN academy_tests_question as atq on atq."id" = oq.academy_question_id
            ORDER BY oq.academy_test_id DESC, oq.atq_index ASC, oq.academy_question_id ASC, oa."sequence" ASC, oa."id" ASC
        """

        drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                _sql_query
            )
        )
