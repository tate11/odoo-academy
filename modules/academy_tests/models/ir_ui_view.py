# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Ir UI View

This module contains the ir.ui.view model extension with an overloaded method
get_view_id to allow access some views and reports from this module throught
Odoo website without restrictions..

Classes:
    IrUIView: This is the unique model class in this module
    and it defines an Odoo model with all its attributes and related behavior.
"""


from logging import getLogger


# pylint: disable=locally-disabled, E0401
from odoo.addons.website.models import ir_ui_view
from odoo import api, tools


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)


# pylint: disable=locally-disabled, R0903
class IrUiView(ir_ui_view.View):
    """ The summary line for a class docstring should fit on one line.
    Fields:
      name (Char): Human readable name which will identify each record.
    """

    _inherit = ['ir.ui.view']


    @api.model
    @tools.ormcache_context('self._uid', 'xml_id', keys=('website_id',))
    def get_view_id(self, xml_id):
        """ When website module is installed, website_id attribute
        stored in context disable report access by url, but this module
        needs to have this access active for some views.
        This overloaded method check if view xml_id is in list then
        removes website_id from context.
        NOTE: This is only a temporal patch, it will be changed by
        another solution.
        """

        views = [
            "academy_tests.at_post_test_question_image",
            "academy_tests.view_at_answer_qweb",
            "academy_tests.view_at_question_qweb",
            "academy_tests.view_at_answers_table_qweb",
            "academy_tests.view_at_test_document_qweb",
            "academy_tests.view_at_test_qweb",
            "academy_tests.action_report_printable_test",
        ]

        ctx = self._context
        if xml_id in views and 'website_id' in ctx:
            ctx = {item:ctx[item] for item in ctx if item != 'website_id'}

        return super(IrUiView, self.with_context(ctx)).get_view_id(xml_id)



