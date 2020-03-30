# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.addons.academy_base.models.lib.custom_model_fields import Many2manyThroughView


from logging import getLogger


_logger = getLogger(__name__)


INHERITED_TOPICS_REL = """
    SELECT
        tree."requested_module_id" as training_module_id,
        link."topic_id" as test_topic_id
    FROM
        academy_training_module_tree_readonly AS tree
    INNER JOIN academy_tests_topic_training_module_link AS link 
        ON tree."responded_module_id" = link."training_module_id"
"""

INHERITED_CATEGORIES_REL = """
    WITH linked AS (
        SELECT
            tree."requested_module_id",
            tree."responded_module_id",
            link."topic_id",
            link_rel."category_id" 
        FROM
            academy_training_module_tree_readonly AS tree
        INNER JOIN academy_tests_topic_training_module_link AS link 
            ON tree."responded_module_id" = link."training_module_id"
        LEFT JOIN academy_tests_category_tests_topic_training_module_link_rel AS link_rel 
            ON link_rel."tests_topic_training_module_link_id" = link."id" 
    ), direct_categories AS ( 
        SELECT 
            requested_module_id,
            topic_id,
            category_id 
        FROM 
            linked 
        WHERE 
            category_id IS NOT NULL 
    ), no_direct_categories AS (
        SELECT
            requested_module_id,
            linked."topic_id",
            atc."id" AS category_id 
        FROM
            linked
        INNER JOIN academy_tests_category AS atc 
            ON atc."topic_id" = linked."topic_id" 
        WHERE
            linked."category_id" IS NULL 
    ), full_set as (
        SELECT
            * 
        FROM
            direct_categories 
        UNION ALL SELECT
            * 
        FROM
            no_direct_categories
        ) SELECT 
            requested_module_id AS training_module_id,
            category_id AS test_category_id
    FROM full_set
"""


class AcademyTrainingModule(models.Model):
    """ Extends academy.training.module to link to training topic

    Fields:
      topic_ids (One2many): Test topics linked to the module record.

    """

    _name = 'academy.training.module'
    _inherit = ['academy.training.module']


    topic_link_ids = fields.One2many(
        string='Topics',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Link test topics to this module',
        comodel_name='academy.tests.topic.training.module.link',
        inverse_name='training_module_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None,
    )

    available_topic_ids = Many2manyThroughView(
        string='Available topics',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.tests.topic',
        relation='academy_training_module_test_topic_rel',
        column1='training_module_id',
        column2='test_topic_id',
        domain=[],
        context={},
        limit=None,
        sql=INHERITED_TOPICS_REL
    )

    available_categories_ids = Many2manyThroughView(
        string='Available categories',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.tests.category',
        relation='academy_training_module_test_category_rel',
        column1='training_module_id',
        column2='test_category_id',
        domain=[],
        context={},
        limit=None,
        sql=INHERITED_CATEGORIES_REL
    )

