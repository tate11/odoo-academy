# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.tools import drop_view_if_exists

from logging import getLogger


_logger = getLogger(__name__)


class AcademyTrainingActionUnitControl(models.Model):
    """ Relationship beetween trainng actions and training units
    """

    _name = 'academy.training.action.unit.control'
    _description = u'Academy training action unit control'

    _rec_name = 'name'
    _order = 'sequence ASC'


    _auto = False
    _table = 'academy_training_action_unit_control'


    # ------------------------ PSEUDO ENTITY FIELDS ---------------------------


    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=True,
        index=False,
        default=False,
        help='Make record visible or not'
    )

    sequence = fields.Integer(
        string='Sequence',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Order of the unit in the action'
    )

    name = fields.Char(
        string='Name',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Code of the training unit',
        size=255,
        translate=True
    )

    overall = fields.Float(
        string='Overall',
        required=False,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Show value for '
    )

    done = fields.Float(
        string='Done',
        required=False,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Show value for '
    )

    remaining = fields.Float(
        string='Remaining',
        required=False,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Show value for '
    )

    overage = fields.Float(
        string='Overage',
        required=False,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Show value for '
    )

    selected = fields.Boolean(
        string='Selected',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help="Allows choosing an unit to be used in session"
    )

    academy_training_unit_id = fields.Many2one(
        string='Training unit id',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Show related training unit',
        comodel_name='academy.training.unit',
        domain=[],
        context={},
        ondelete='restrict',
        auto_join=False
    )

    academy_training_action_id = fields.Many2one(
        string='Training action id',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Show related training action',
        comodel_name='academy.training.action',
        domain=[],
        context={},
        ondelete='restrict',
        auto_join=False
    )


    # ---------------------- DETABASE MODEL DEFINITION ------------------------


    @api.model_cr
    def init(self):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        sql_query = """
            SELECT

                -- Entity identifier. You must keep same order in ORDER BY clausule
                (
                    "row_number"() OVER(
                        ORDER BY ata."id" ASC,
                        acu."id" ASC,
                        acu."sequence" ASC,
                        atu."sequence" ASC
                    )
                ) :: INT AS "id",

                -- Entity requited fields, their come from training action
                ata.create_date,
                ata.write_date,
                ata.create_uid,
                ata.write_uid,

                -- This will be active only if all related models are active
                (atu.active and atm.active and acu.active and apq.active and ata.active) :: BOOLEAN as active,

                -- Related action and unit
                ata."id" AS academy_training_action_id,
                atu."id" AS academy_training_unit_id,

                -- Sequence of the units (all) by action
                "row_number"() OVER(PARTITION BY ata."id") as "sequence",

                -- Fields for time control
                atu.hours AS overall,
                COALESCE (ati.hours, 0) AS done,
                GREATEST(0,(atu.hours - COALESCE(ati.hours, 0))) :: FLOAT as remaining,
                ABS(LEAST(0,(atu.hours - COALESCE(ati.hours, 0)))) :: FLOAT as overage,

                -- Unit name, it will be used in _rec_name
                atu."name" as "name",

                -- Fake field the allows user to select record
                FALSE :: BOOLEAN AS selected

            FROM
                academy_training_unit AS atu

            INNER JOIN academy_training_module AS atm
                ON atu.academy_training_module_id = atm."id"

            INNER JOIN academy_competency_unit AS acu
                ON acu.academy_training_module_id = atm."id"

            INNER JOIN academy_professional_qualification AS apq
                ON apq."id" = acu.professional_qualification_id

            INNER JOIN academy_training_action AS ata
                ON ata.professional_qualification_id = apq."id"

/*            LEFT JOIN academy_training_session_itemization AS ati
                ON ati.academy_training_unit_id = atu."id"
*/
            ORDER BY ata."id" ASC,
                acu."id" ASC,
                acu."sequence" ASC,
                atu."sequence" ASC
        """

        drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                sql_query
            )
        )


    # --------------------------- PUBLIC METHODS ------------------------------

    @api.multi
    def append_unit(self, arg):
        print (self, arg, self.env.context)