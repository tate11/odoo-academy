# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.tools import drop_view_if_exists
from logging import getLogger


_logger = getLogger(__name__)


class AcademyTrainingModuleTreeReadonly(models.Model):
    """ This model allows to query a module returning a recordset with:
    	- The own module
    	- The child modules
    	- The parent module

    	This model is used by others to get all available records that were 
    	linked to a complete training module or to all of its training units
    """

    _name = 'academy.training.module.tree.readonly'
    _description = u'Academy training module tree readonly'

    _rec_name = 'requested_module_id'
    _order = 'requested_module_id ASC,  responded_module_id ASC'
    _auto = False

    _view_sql = '''
		WITH own_id AS (
			-- Request modules by id and respond with the own id
			SELECT
				"create_uid",
				"create_date",
				"write_uid",
				"write_date",
				"id" AS requested_module_id,
				"id" AS responded_module_id,
				"training_module_id" AS parent_module_id
			FROM 
				academy_training_module
		),	parent_id AS (
			-- Request modules by own id and respond with the parent id
			SELECT
				"create_uid",
				"create_date",
				"write_uid",
				"write_date",
				"id" AS requested_module_id,
				"training_module_id" AS responded_module_id,
				null::integer AS parent_module_id
			FROM 
				academy_training_module 
			WHERE
				training_module_id IS NOT NULL
		), child_id AS (
			-- Request modules by parent id and respond with own id
			SELECT
				"create_uid",
				"create_date",
				"write_uid",
				"write_date",
				"training_module_id" AS requested_module_id,
				"id" AS responded_module_id,
				training_module_id AS parent_module_id 
			FROM
				academy_training_module 
			WHERE
				training_module_id IS NOT NULL	
		), full_set as (
			-- Merge all queries into a single recordset
			SELECT
			* 
			FROM
				own_id 
			UNION ALL SELECT
				* 
			FROM
				parent_id 
			UNION ALL SELECT
				* 
			FROM
				child_id
		) SELECT
			"create_uid",
			"create_date",
			"write_uid",
			"write_date",
			requested_module_id,
			responded_module_id,
			parent_module_id
		FROM 
			full_set
		ORDER BY 
			requested_module_id ASC, 
			responded_module_id ASC
    '''


    requested_module_id = fields.Many2one(
        string='Requested module',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help='Parent module',
        comodel_name='academy.training.module',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    parent_module_id = fields.Many2one(
        string='Parent module',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Parent module',
        comodel_name='academy.training.module',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    responded_module_id = fields.Many2one(
        string='Responded module id',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help='Parent module',
        comodel_name='academy.training.module',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )


    def init(self):
        drop_view_if_exists(self.env.cr, self._table)

        self.env.cr.execute('''CREATE or REPLACE VIEW {} as (
            {}
        )'''.format(self._table, self._view_sql))
