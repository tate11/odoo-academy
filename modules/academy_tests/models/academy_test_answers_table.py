# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0212,E0611,C0103,R0903,C0111,F0401
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools import drop_view_if_exists
from logging import getLogger


_logger = getLogger(__name__)


class AcademyAnswersTable(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.test.answers.table'
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
        comodel_name='academy.test',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    academy_test_question_id = fields.Many2one(
        string='Question',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Question to which this answer belongs',
        comodel_name='academy.test.question',
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
                    academy_test_answer."id",
                    (row_number() OVER (PARTITION BY academy_test_answer.academy_test_question_id ORDER BY academy_test_answer.academy_test_question_id ASC, academy_test_answer."sequence", academy_test_answer."id"))::integer AS "sequence",
                    academy_test_answer.academy_test_question_id,
                    academy_test_answer.is_correct
                FROM academy_test_answer
                WHERE active = TRUE
                ORDER BY academy_test_answer.academy_test_question_id ASC, academy_test_answer."sequence", academy_test_answer."id"

            ), ordered_quesions AS (

            -- Ensure questions sequence
                SELECT
                    rel.academy_test_id,
                    rel.academy_test_question_id,
                    ROW_NUMBER() OVER(PARTITION BY rel.academy_test_id ORDER BY  rel.academy_test_id DESC, rel."sequence" ASC, rel.academy_test_question_id ASC) as atq_index
                    FROM academy_test_academy_test_question_rel AS rel
                    WHERE active = TRUE
                ORDER BY rel.academy_test_id DESC, rel."sequence" ASC, rel.academy_test_question_id ASC

            )

            -- Main query
            SELECT
                ROW_NUMBER() OVER(ORDER BY oq.academy_test_id DESC, oq.atq_index ASC, oq.academy_test_question_id ASC, oa."sequence" ASC, oa."id" ASC)::INTEGER AS "id",
                oq.academy_test_id::INTEGER,
                oq.academy_test_question_id::INTEGER,
                oa."id"::INTEGER as academy_answer_id,
                oq.atq_index::INTEGER as "sequence",
                SUBSTRING('ABCDEFGHIJKLMNOPQRSTUVWXYZ' FROM oa."sequence" FOR 1)::VARCHAR AS "name",
                atq."description"::TEXT
            FROM ordered_quesions as oq
            LEFT JOIN (SELECT * FROM ordered_answers WHERE is_correct IS TRUE) as oa on oq.academy_test_question_id = oa.academy_test_question_id
            LEFT JOIN academy_test_question as atq on atq."id" = oq.academy_test_question_id
            ORDER BY oq.academy_test_id DESC, oq.atq_index ASC, oq.academy_test_question_id ASC, oa."sequence" ASC, oa."id" ASC
        """

        drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                _sql_query
            )
        )
