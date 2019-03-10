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
from dicttoxml import dicttoxml
from lxml import etree
from re import sub as replace, UNICODE

from openerp.http import route, request, Controller, Response
from openerp.tools.translate import _
from openerp.addons.web.controllers.main import serialize_exception, content_disposition
from odoo.tools import ustr


_logger = getLogger(__name__)

tkeys = ['id', 'name', 'description', 'preamble']
qkeys = ['id', 'name', 'description', 'preamble', 'type_id']
akeys = ['id', 'name', 'is_correct', 'description']
ckeys = ['id', 'name', 'description']
pkeys = ['id', 'name', 'description']

class PublishResources(Controller):
    """ Allow teachers to publish tests through Odoo website
    """



    @route('/academy/download/test', type='http', auth='user', website=True)
    def download_test(self, **kw):
        """ Allow users to download test for given test_id """
        ext = kw.get('type', 'pdf').lower()
        test_id = self._safe_cast(kw['test_id'], int, False)

        if 'test_id' in kw.keys() and test_id:

            name = self._get_test_name(test_id)
            if not name:
                return Response(status=404)

            if ext in ['pdf', 'html']:
                act_xid = 'academy_tests.action_report_printable_test'
                act_xid = kw.get('act_xid', act_xid).lower()
                return self._make_report_response(test_id, ext, name, act_xid)

            if ext in ['md', 'mkd', 'markdown']:
                return self._make_text_response(test_id, ext, name)

        return Response(status=400)


    def _make_report_response(self, test_id, ext, name, act_xid):

        act_set = self._get_resource_by_ref(act_xid)

        data = self._render_report(act_set, test_id, ext)
        headers = self._build_headers(name, ext)
        response = request.make_response(data, headers)

        return response

    def _make_text_response(self, test_id, ext, name):
        test_obj = request.env['academy.tests.test']
        test_set = test_obj.browse(test_id)

        question_set = test_set .question_ids
        tdata = ''

        qindex = 1
        for qitem in question_set:
            tdata = tdata + self._line_break()

            tdata = tdata + self._read_attachments(qitem)
            tdata = tdata + self._read_statement(qitem, qindex)
            tdata = tdata + self._read_answers(qitem)

        tdata = tdata + self._line_break(tdata)


        headers = self._build_headers(name, ext)
        return request.make_response(tdata, headers)


    def _read_statement(self, qitem, qindex):
        tdata = ''


        if qitem.description:
            text = self._clear_text(qitem.description)
            tdata = tdata + '\n> {}'.format(text)

        if qitem.preamble:
            text = self._clear_text(qitem.preamble)
            tdata = tdata + '\n{}'.format(text)

        text = self._clear_text(qitem.name)
        tdata = '\n{}. {}'.format(qindex, text)

        return tdata


    def _read_attachments(self, qitem):
        tdata = ''

        url = 'http://localhost:50110/academy/download/attachment?id='
        for ira in qitem.ir_attachment_ids:
            tdata = tdata + '\n![{}]({}{})'.format(
                ira.name,
                url,
                ira.id
            )

        return tdata


    def _read_answers(self, qitem):
        tdata = ''

        aindex = 1
        for aitem in qitem.answer_ids:
            text = self._clear_text(aitem.name)
            letter = 'x' if aitem.is_correct else chr(96 + aindex)
            tdata = tdata + '\n{}) {}'.format(letter, text)
            aindex = aindex + 1

        return tdata


    @staticmethod
    def _line_break(condition=True):
        return '\n'

    @staticmethod
    def _clear_text(text):
        text = replace(r'(^[\t  ])|([\t  ]+$)', r'', text, UNICODE)
        text = replace(r'( +)', r' ', text, UNICODE)
        text = replace(r'[\n\n]+', '\n', text, UNICODE)

        return text

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
        """ Retrieves the report action with given external id
        """

        module, name = external_id.split('.')

        md_obj = request.env['ir.model.data']
        model, res_id = md_obj.get_object_reference(module, name)

        return request.env[model].browse(res_id)


    @staticmethod
    def _without_website_id(obj_set):
        """ Removes website_id from context. This is used to allow publish
        test reports directly using URL
        """

        ctx = dict(request.context)
        ctx = {item:ctx[item] for item in ctx if item != 'website_id'}

        return obj_set.with_context(ctx)


    @staticmethod
    def _safe_cast(val, to_type, default=None):
        """ Cast a given string consisting of numerical digits to a true
        python numerical value. This is used to convert ids passing in URL
        to a real record id
        """
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default


    def _build_headers(self, name, ext):
        """ Builds http headers needed to send published tests.
        Returned mimetypes in header can be: text/html, application/pdf or,
        In any other case, text/markdown
        """

        filename = ustr('{}.{}'.format(name, ext))
        filename = urls.url_quote(filename)

        # pdf, html or markdown
        mkd = 'text/markdown; charset=utf-8'
        mime = mimetypes.types_map.get('.{}'.format(ext), mkd)
        disposition = "inline; filename*=UTF-8''%s" % filename

        headers = [
            ('Content-Type', mime),
            ('Content-Disposition', disposition)
        ]

        return headers



    # --------------- FOLLOWING LINES CAN BE USEFUL IN FUTURE -----------------

    # @staticmethod
    # def _get_questions(test):
    #     rels = test.question_ids.sorted(lambda item: item.sequence)
    #     return rels.mapped('question_id')


    # @staticmethod
    # def _get_value(obj, key):
    #     value = getattr(obj, key)

    #     if hasattr(value, 'id'):
    #         value = value.id

    #     return value


    # def _get_values(self, obj, keys):
    #     result = {}

    #     for key in keys:
    #         result[key] = self._get_value(obj, key)

    #     return result


    # @route('/academy/serialize/test', type='http', auth='user', website=True)
    # def serialize_test(self, **kw):
    #     """ Export test as JSON or XML
    #     """

    #     test_obj = request.env['academy.tests.test']
    #     test_set = test_obj.browse(int(kw['test_id']))

    #     test = self._get_values(test_set, tkeys)

    #     test['questions'] = []
    #     qindex = 0

    #     for question in self._get_questions(test_set):
    #         test['questions'].append(self._get_values(question, qkeys))

    #         aindex = 0
    #         test['questions'][qindex]['answers'] = []
    #         for answer in question.answer_ids:
    #             answerdict = self._get_values(answer, akeys)
    #             test['questions'][qindex]['answers'].append(answerdict)
    #             aindex = aindex + 1

    #         test['questions'][qindex]['topic'] = \
    #             self._get_values(question.topic_id, pkeys)

    #         cindex = 0
    #         test['questions'][qindex]['categories'] = []
    #         for category in question.category_ids:
    #             catdict = self._get_values(category, ckeys)
    #             test['questions'][qindex]['categories'].append(catdict)
    #             cindex = cindex + 1

    #         qindex = qindex + 1


    #     result1 = request.make_response(dicttoxml(test), \
    #         [('Content-Type', 'text/xml; charset=utf-8')])

    #     result2 = request.make_response(json.dumps(test), \
    #         [('Content-Type', 'application/json; charset=utf-8')])

    #     return result2

