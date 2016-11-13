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
             WITH ordered_answers AS (
                     SELECT at_answer.id,
                        (row_number() OVER (PARTITION BY at_answer.at_question_id ORDER BY at_answer.sequence))::integer AS sequence,
                        at_answer.at_question_id,
                        at_answer.is_correct
                       FROM at_answer
                      ORDER BY (row_number() OVER (PARTITION BY at_answer.at_question_id ORDER BY at_answer.sequence))::integer
                    )
             SELECT row_number() OVER () AS id,
                att.id AS at_test_id,
                atq.id AS at_question_id,
                ata.id AS at_answer_id,
                rel.sequence,
                    CASE
                        WHEN (ata.id IS NOT NULL) THEN substr('ABCDEFGHIJKLMNOPQRSTUVWXYZ'::text, ata.sequence, 1)
                        ELSE NULL::text
                    END AS name,
                atq.description
               FROM (((at_test_at_question_rel rel
                 JOIN at_test att ON ((att.id = rel.at_test_id)))
                 JOIN at_question atq ON ((rel.at_question_id = atq.id)))
                 LEFT JOIN ( SELECT ordered_answers.id,
                        ordered_answers.sequence,
                        ordered_answers.at_question_id,
                        ordered_answers.is_correct
                       FROM ordered_answers
                      WHERE (ordered_answers.is_correct = true)) ata ON ((ata.at_question_id = atq.id)))
              ORDER BY att.id, rel.sequence, ata.sequence
        """

        drop_view_if_exists(cr, self._table)
        cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )
