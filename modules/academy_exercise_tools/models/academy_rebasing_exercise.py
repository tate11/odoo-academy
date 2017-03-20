# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger
from openerp.tools import drop_view_if_exists

_logger = getLogger(__name__)


class AcademyRebasingExercise(models.Model):
    """ Exercise

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.rebasing.exercise'
    _description = u'Academy rebasing exercise'

    _table = 'academy_rebasing_exercise'
    _auto = False

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        readonly=True,
        index=True,
        default=None,
        help='Exercise name',
        size=50,
        translate=True
    )

    academy_rebasing_exercise_item_ids = fields.One2many(
        string='Exercise items',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help='List with all items',
        comodel_name='academy.rebasing.exercise.item',
        inverse_name='academy_rebasing_exercise_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    @api.model_cr
    def init(self):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        self._sql_query = """
            WITH TDATA AS (
                SELECT DISTINCT
                    academy_rebasing_exercise_id AS "id",
                    'EJERCICIO DE CAMBIOS DE BASE ' || TO_CHAR(CURRENT_TIMESTAMP, '(YYYY-MM-DD)') || ' - ' as "name"
                FROM
                    academy_rebasing_exercise_item
                ORDER BY academy_rebasing_exercise_id
            ) SELECT
                "id"::INT as "id",
                1::INT AS create_uid,
                (to_char(now(), 'YYYY-MM-DD HH24:MI:SS'::text))::timestamp without time zone AS create_date,
                1::INT AS write_uid,
                (to_char(now(), 'YYYY-MM-DD HH24:MI:SS'::text))::timestamp without time zone AS write_date,
                ("name" || LPAD((ROW_NUMBER() OVER(ORDER BY "id"))::VARCHAR, 2, '0'))::VARCHAR AS "name"
            FROM TDATA
        """

        drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )
