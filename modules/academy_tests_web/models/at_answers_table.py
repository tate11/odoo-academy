# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0212,E0611,C0103,R0903,C0111,F0401
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields
from openerp.tools import drop_view_if_exists
from logging import getLogger


_logger = getLogger(__name__)


class AtAnswersTable(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'at.answers.table'
    _description = u'At answers table'

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

    at_test_id = fields.Many2one(
        string='Test',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Test to which this question belongs',
        comodel_name='at.test',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    at_question_id = fields.Many2one(
        string='Question',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Question to which this answer belongs',
        comodel_name='at.question',
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


    def init(self, cr):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        self._sql_query = u"""
            WITH right_answers AS (
                WITH answers AS (
                    SELECT
                        "id",
                        "row_number" () OVER (
                            PARTITION BY at_question_id
                            ORDER BY
                                at_question_id ASC,
                                "sequence" ASC
                        )::INT as answer,
                        is_correct,
                        at_question_id
                    FROM
                        at_answer
                ) SELECT
                    *
                FROM
                    "answers"
                WHERE
                    is_correct = TRUE
            ) SELECT
                "row_number"() over() as id,
                atqr.at_test_id as at_test_id,
                atqr.at_question_id as at_question_id,
                ra."id" as at_answer_id,
                ROW_NUMBER () OVER (
                        PARTITION BY at_test_id
                        ORDER BY
                            at_test_id ASC,
                            atqr.at_question_id asc
                    )::INT AS "sequence",
                substr('ABCDEFGHIJKLMNOPQRSTUVWXYZ', ra.answer, 1) as "name",
                description -- regexp_replace(atq.description, E'[\\r\\n]+', E'\\t', 'g')::TEXT as
            FROM
                at_test_at_question_rel atqr
            LEFT JOIN right_answers AS ra ON atqr.at_question_id = ra.at_question_id
            inner join at_question as atq on atq.id = atqr.at_question_id
        """

        drop_view_if_exists(cr, self._table)
        cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )
