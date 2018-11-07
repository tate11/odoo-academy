#pylint: disable=I0011,W0212,C0111,F0401,R0903
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, registry
from openerp.tools import config
import os
import re
import zipfile
import psycopg2
from . import custom_model_fields

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

import base64

from logging import getLogger
_logger = getLogger(__name__)



class AcademyTrainingResource(models.Model):
    """ Resource will be used in a training unit or session

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.resource'
    _description = u'Academy training resource'

    _rec_name = 'name'
    _order = 'name ASC'

    _inherit = ['mail.thread']

    # ---------------------------- ENTITY FIELDS ------------------------------


    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help=False,
        size=254,
        translate=True
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Enter new description',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Enables/disables the record'
    )

    manager_id = fields.Many2one(
        string='Manager',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=u'False',
        comodel_name='res.users',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    last_update = fields.Date(
        string='Last update',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help=u'Last update'
    )

    academy_training_unit_ids = fields.Many2many(
        string='Training units',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.unit',
        # relation='model_name_this_model_rel',
        # column1='model_name_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    ir_attachment_ids = fields.Many2many(
        string='Attachments',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=u'Resources stored in database',
        comodel_name='ir.attachment',
        # relation='ir_attachment_this_model_rel',
        # column1='ir_attachment_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    directory = fields.Char(
        string='Directory',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Directory which contains resource files',
        size=260,
        translate=True
    )

    directory_file_ids = fields.One2many(
        string='Directory files',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.resource.file',
        inverse_name='academy_training_resource_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    academy_training_action_ids = custom_model_fields.Many2ManyThroughView(
        string='Training actions',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Choose related training actions',
        comodel_name='academy.training.action',
        relation='academy_training_action_academy_training_resource_rel',
        column1='academy_training_resource_id', # this is the name in the SQL VIEW
        column2='academy_training_action_id',   # this is the name in the SQL VIEW
        domain=[],
        context={},
        limit=None
    )

    # --------------------------- COMPUTED FIELDS -----------------------------


    attachmentcounting = fields.Integer(
        string='Attachments',
        required=False,
        readonly=False,
        index=False,
        default=0,
        help='Number of attachments in resource',
        compute='_compute_attachmentcounting',
    )

    directory_filecounting = fields.Integer(
        string='Files',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Number of files in related directory',
        compute='_compute_directory_filecounting',
    )


    # ---------------------- FIELD METHODS AND EVENTS -------------------------


    @api.multi
    @api.depends('ir_attachment_ids')
    def _compute_attachmentcounting(self):
        """ Computes the number of ir.attachment records related with resource
        """

        for record in self:
            record.attachmentcounting = len(record.ir_attachment_ids)


    @api.multi
    @api.depends('directory_file_ids')
    def _compute_directory_filecounting(self):
        """ Computes the number of files in resource related directory
        """

        for record in self:
            record.directory_filecounting = len(record.directory_file_ids)


    # --------------------------- PUBLIC METHODS ------------------------------

    def _reload_single_directory(self):
        """ Reload directory filenames
        """
        record = self
        if record.directory:
                base_path = os.path.abspath(record.directory)

                # Remove all current file names
                record.directory_file_ids = [
                    (2, _id) for _id in record.directory_file_ids.mapped('id')
                ]

                filenames = []

                #pylint: disable=I0011,W0612
                for root, dirs, files in os.walk(base_path):
                    for name in files:
                        rel_path = os.path.join(root, name).replace(base_path + '\\', '')

                        if  re.search('^[^~_]', rel_path):
                            filenames.append(
                                (0, 0, {
                                    'name': rel_path,
                                    'academy_training_resource_id': record.id
                                    }
                                )
                            )

                record.directory_file_ids = filenames

    # @api.one
    @api.onchange('directory')
    def _onchange_directory(self):
        """ Onchange event for general_public_access field
        """

        self._reload_single_directory()



    @api.multi
    def reload_directory(self):
        """ Reload directory filenames
        """

        for record in self:
            record._reload_single_directory()

    @staticmethod
    def _zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                relpath = os.path.relpath(root, path)
                relfile = os.path.join(relpath, file)
                _logger.debug(u'### Zipping {}'.format(relfile))
                ziph.write(os.path.join(root, file), relfile)

    @api.multi
    def download_directory(self):
        data_dir = config['data_dir']
        data_dir = os.path.abspath(data_dir)

        for record in self:
            zipname = u'{}.zip'.format(record.name)
            #zippath = os.path.join(data_dir, zipname)
            #_logger.debug(zippath)
            #_logger.debug(self.directory)
            in_memory = BytesIO()
            zipf = zipfile.ZipFile(in_memory, 'w', zipfile.ZIP_DEFLATED)
            self._zipdir(self.directory, zipf)
            _logger.debug(in_memory.getbuffer().nbytes)
            zipf.close()

            datas = base64.b64encode(in_memory.getvalue())
            _logger.debug(u'zip size: {}'.format(len(datas)))
            attach_obj = self.env['ir.attachment']
            attach_obj.create({'name': zipname,
                               'datas': datas,
                               'datas_fname': zipname,
                               'res_model': self._name,
                               'res_id': self.id})


