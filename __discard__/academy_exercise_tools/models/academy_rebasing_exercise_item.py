# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger
from openerp.tools import drop_view_if_exists

_logger = getLogger(__name__)


class AcademyRebasingExerciseItem(models.Model):
    """ Gets random number in decimal, hexadecimal and octal base.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.rebasing.exercise.item'
    _description = u'Academy rebasing exercise item'

    _auto = False
    _table = 'academy_rebasing_exercise_item'

    _rec_name = 'decimal'
    _order = 'id ASC'


    value = fields.Integer(
        string='Decimal',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help='Integer value'
    )

    decimal = fields.Char(
        string='Decimal',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help='Decimal base number',
        size=3,
        translate=True
    )

    binary = fields.Char(
        string='Binary',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help='Binary base number',
        size=8,
        translate=True
    )

    hexadecimal = fields.Char(
        string='Hexadecimal',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help='Hexadecimal base number',
        size=2,
        translate=True
    )

    octal = fields.Char(
        string='Octal',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help='Octal base number',
        size=3,
        translate=True
    )

    academy_rebasing_exercise_id = fields.Many2one(
        string='Academy rebasing exercise',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help='Exercise to witch this item belongs',
        comodel_name='academy.rebasing.exercise',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )


    @api.model_cr
    def init(self):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        self._sql_query = """
            WITH ITEMS AS (
                WITH RANDOM_VALUES AS (
                    SELECT
                         (random()*255)::int AS "dec"
                    FROM
                         generate_series (1, 1000) AS x(n)
                ) SELECT DISTINCT ON ("dec")
                    "dec"::INTEGER AS VALUE,
                    LPAD("dec"::VARCHAR, 3, '0')::VARCHAR AS "decimal",
                    ("dec"::BIT(8))::VARCHAR AS "binary",
                    UPPER(LPAD(to_hex("dec")::TEXT, 2, '0')) as "hexadecimal",
                    LPAD(((SELECT ARRAY_TO_STRING(ARRAY_AGG("value"), '') FROM (SELECT (UNNEST(regexp_matches((dec::BIT(9))::TEXT, '...', 'g'))::BIT(3)::INTEGER) AS "value") as T)::INTEGER)::VARCHAR, 3, '0')::VARCHAR AS "octal"
                FROM RANDOM_VALUES LIMIT 50
                ) SELECT
                    ROW_NUMBER() OVER() AS "id",
                    1::INTEGER AS create_uid,
                    TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI:SS')::TIMESTAMP as create_date,
                    1::INTEGER AS write_uid,
                    TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-MM-DD HH24:MI:SS')::TIMESTAMP as write_date,
                    *,
                                        (ROW_NUMBER() OVER() % 10 + 1)::INTEGER AS academy_rebasing_exercise_id
            FROM ITEMS
        """

        drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )
