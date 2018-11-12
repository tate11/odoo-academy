# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo.addons.website.models import ir_ui_view
from openerp import models, fields, api, tools
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


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
	    	"academy_tests.academy_post_test_question_image",
			"academy_tests.view_academy_answer_qweb",
			"academy_tests.view_academy_question_qweb",
			"academy_tests.view_academy_answers_table_qweb",
			"academy_tests.view_academy_test_document_qweb",
			"academy_tests.view_academy_test_qweb",
			"academy_tests.action_report_printable_test",
    	]

    	ctx = self.env.context
    	if xml_id in views and 'website_id' in ctx:
    		ctx = {item:ctx[item] for item in ctx if item!='website_id'}
    		print('In', self.with_context(ctx)._context)

    	return super(IrUiView, self.with_context(ctx)).get_view_id(xml_id)







