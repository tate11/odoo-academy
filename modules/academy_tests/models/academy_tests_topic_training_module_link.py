# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################


from odoo import models, fields, api
from odoo.tools.translate import _


from logging import getLogger


_logger = getLogger(__name__)


class AcademyTestsTopicTrainingModuleLink(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.tests.topic.training.module.link'
    _description = u'Academy tests, topic-training module link'

    _rec_name = 'topic_id'
    _order = 'topic_id ASC'


    topic_id = fields.Many2one(
        string='Topic',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Topic will be linked to the module',
        comodel_name='academy.tests.topic',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False,
    )

    training_module_id = fields.Many2one(
        string='Training module',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Module will be linked to the topic',
        comodel_name='academy.training.module',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    category_ids = fields.Many2many(
        string='Categories',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Categories relating to this question',
        comodel_name='academy.tests.category',
        relation='academy_tests_category_tests_topic_training_module_link_rel',
        column1='tests_topic_training_module_link_id',
        column2='category_id',
        domain=[],
        context={},
        limit=None,
        track_visibility='onchange',
    )

    sequence = fields.Integer(
        string='Sequence',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help='Choose the unit order'
    )


    @api.onchange('topic_id')
    def _onchange_academy_topid_id(self):
        """ Updates domain form category_ids, this shoud allow categories
        only in the selected topic.
        """
        topic_set = self.topic_id
        valid_ids = topic_set.category_ids & self.category_ids

        self.category_ids = [(6, None, valid_ids.mapped('id'))]

    _sql_constraints = [
        (
            'unique_topic_id_training_module_id',
            'UNIQUE(topic_id, training_module_id)',
            _(u'Each topic can only be linked once')
        )
    ]


    # def _get_all_topic_categories(self, topic_id=None):
    #     if not topic_id:
    #         topic_id = self.topic_id.id

    #     category_domain = [('topic_id', '=', topic_id)]
    #     category_obj = self.env['academy.tests.category']
    #     category_set = category_obj.search(category_domain)

    #     return category_set


    # @api.model
    # def create(self, values):
    #     """
    #         Create a new record for a model AcademyTestsTopicTrainingModuleLink
    #         @param values: provides a data for new record
    
    #         @return: returns a id of new record
    #     """
    
    #     if 'topic_id' in values.keys() and not 'category_ids' in values.keys():
    #         topic_id = values.get('topic_id', False)
    #         if topic_id:
    #             category_ids = self._get_all_topic_categories(topic_id)
    #             if category_ids:
    #                 values['category_ids'] = [[6, False, category_ids.mapped('id')]]
            

    #     result = super(AcademyTestsTopicTrainingModuleLink, self).create(values)
    
    #     return result


    # def write(self, values):
    #     """
    #         Update all record(s) in recordset, with new value comes as {values}
    #         return True on success, False otherwise
    
    #         @param values: dict of new values to be set
    
    #         @return: True on success, False otherwise
    #     """

    #     result = super(AcademyTestsTopicTrainingModuleLink, self).write(values)

    #     if result and self.topic_id and not self.category_ids:
    #         category_ids = self._get_all_topic_categories()
    #         if category_ids:
    #             values = {'category_ids' : [[6, False, category_ids.mapped('id')]] }
    #             result = super(AcademyTestsTopicTrainingModuleLink, self).write(values)
    
    #     return result