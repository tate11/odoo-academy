# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################
#pylint: disable=I0011,R0201,R0903,C0103,W0611,F0401,W0613,W0612,W0703

import json
import base64
import mimetypes
from logging import getLogger
from io import BytesIO
from werkzeug import urls

from openerp.http import route, request, Controller, Response
from openerp.tools.translate import _
from openerp.addons.web.controllers.main import serialize_exception, content_disposition
from odoo.tools import ustr


_logger = getLogger(__name__)


class PublishResources(Controller):
    """ Allow teachers to publish tests through Odoo website
    """

    @route('/academy/download/test', type='http', auth='user', website=True)
    def download_test(self, **kw):
        """ Allow users to download test for given test_id """

        act_xid = 'academy_tests.action_report_printable_test'
        act_xid = kw.get('act_xid', act_xid).lower()
        ext = kw.get('type', 'pdf').lower()

        if 'test_id' not in kw.keys():
            return Response(status=400)

        test_id = self._safe_cast(kw['test_id'], int, False)
        if not test_id:
            return Response(status=400)

        name = self._get_test_name(test_id)
        if not name:
            return Response(status=404)

        act_set = self._get_resource_by_ref(act_xid)
        if not test_id:
            return Response(status=400)

        data = self._render_report(act_set, test_id, ext)
        headers = self._build_headers(name, ext)
        response = request.make_response(data, headers)

        return response


    @route('/academy/download/answers', type='http', auth='user', website=True)
    def download_answers(self, **kw):
        """ Allow users to download answers table for given test_id """

        act_xid = 'academy_tests.action_report_printable_answer_table'
        act_xid = kw.get('act_xid', act_xid).lower()
        ext = kw.get('type', 'pdf').lower()

        if 'test_id' not in kw.keys():
            return Response(status=400)

        test_id = self._safe_cast(kw['test_id'], int, False)
        if not test_id:
            return Response(status=400)

        name = self._get_test_name(test_id)
        if not name:
            return Response(status=404)

        act_set = self._get_resource_by_ref(act_xid)
        if not test_id:
            return Response(status=400)

        data = self._render_report(act_set, test_id, ext)
        headers = self._build_headers(name, ext)
        response = request.make_response(data, headers)

        return response


    @route('/academy/download/attachment', type='http', auth="public")
    @serialize_exception
    def download_attachment(self, **kw):
        """ Download link for files stored as binary fields.

        :param str model: name of the model to fetch the binary from
        :param str field: binary field
        :param str id: id of the record from which to fetch the binary
        :param str filename: field holding the file's name, if any

        :return: :class:`werkzeug.wrappers.Response`
        """


        ir_attachment_domain = [('id', '=', int(kw['id']))]
        ir_attachment_obj = request.env['ir.attachment']
        ir_attachment_set = ir_attachment_obj.search(ir_attachment_domain)

        filename = ir_attachment_set.datas_fname
        filecontent = base64.b64decode(ir_attachment_set.datas or '')

        if not filecontent:
            return request.not_found()

        return request.make_response(filecontent, \
            [('Content-Type', ir_attachment_set.mimetype), \
            ('Content-Disposition', content_disposition(filename))])


    @staticmethod
    def _get_test_name(res_id):
        """ Checks if exist a `model` record with given `id`

        @param model: odoo model name (NOT the external model name)
        @param res_id: identifier of the record will be checked
        """

        model_obj = request.env['academy.tests.test']
        model_set = model_obj.browse(res_id)

        return model_set.name if model_set.exists() else False


    def _render_report(self, act_set, report_id, ext='pdf'):
        """ Builds a responde with a rendered report in HTML or PDF

        @param act_xid: report action will be used to render report
        @param report_id: id of the report record will be rendered
        @param ext: file extension (without dot)
        """

        # STEP 1: Ensure is valid extension
        ext = ext if ext in ['pdf', 'html'] else 'pdf'

        # STEP 2: Removes website from context
        # website key in context prevents template can be rendered through the web
        act_set = self._without_website_id(act_set)

        # STEP 3: Calls the specific PDF or HTML report action render method
        render_func = getattr(act_set, 'render_qweb_' + ext, None)
        data = render_func([report_id]) # pylint: disable=locally-disabled, E1102

        # STEP 4: return binary data
        return data


    @staticmethod
    def _get_resource_by_ref(external_id):
        module, name = external_id.split('.')

        md_obj = request.env['ir.model.data']
        model, res_id = md_obj.get_object_reference(module, name)

        return request.env[model].browse(res_id)


    @staticmethod
    def _without_website_id(obj_set):
        ctx = dict(request.context)
        ctx = {item:ctx[item] for item in ctx if item != 'website_id'}

        return obj_set.with_context(ctx)


    @staticmethod
    def _safe_cast(val, to_type, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default


    def _build_headers(self, name, ext):
        filename = ustr('{}.{}'.format(name, ext))
        filename = urls.url_quote(filename)

        mime = mimetypes.types_map['.{}'.format(ext)]
        disposition = "inline; filename*=UTF-8''%s" % filename

        headers = [
            ('Content-Type', mime),
            ('Content-Disposition', disposition)
        ]

        return headers
