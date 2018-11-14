# -*- coding: utf-8 -*-
""" AcademyTrainingAction

This module contains the academy.action.resource Odoo model which stores
all training action attributes and behavior.

"""


from logging import getLogger

import os
import re
import zipfile
import base64


# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.tools import config
from . import custom_model_fields

try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO


# pylint: disable=locally-disabled, c0103
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

    _inherit = ['academy.abstract.image', 'mail.thread']

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

    training_module_ids = fields.Many2many(
        string='Training modules',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.module',
        relation='academy_training_module_training_resource_rel',
        column1='training_resource_id',
        column2='training_module_id',
        domain=[],
        context={},
        limit=None
    )

    # pylint: disable=locally-disabled, W0212
    training_unit_ids = fields.Many2many(
        string='Training units',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.unit',
        relation='academy_training_unit_training_resource_rel',
        column1='training_resource_id',
        column2='training_unit_id',
        domain=lambda self: self._domain_for_training_unit_ids(),
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
        relation='academy_training_resource_ir_attachment_rel',
        column1='training_resource_id',
        column2='ir_attachment_id',
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
        inverse_name='training_resource_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    training_action_ids = custom_model_fields.Many2ManyThroughView(
        string='Training actions',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Choose related training actions',
        comodel_name='academy.training.action',
        relation='academy_training_action_training_resource_rel',
        column1='training_resource_id', # this is the name in the SQL VIEW
        column2='training_action_id',   # this is the name in the SQL VIEW
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

    @api.multi
    @api.depends('ir_attachment_ids')
    def _compute_attachmentcounting(self):
        """ Computes the number of ir.attachment records related with resource
        """

        for record in self:
            record.attachmentcounting = len(record.ir_attachment_ids)


    directory_filecounting = fields.Integer(
        string='Files',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Number of files in related directory',
        compute='_compute_directory_filecounting',
    )


    @api.multi
    @api.depends('directory_file_ids')
    def _compute_directory_filecounting(self):
        """ Computes the number of files in resource related directory
        """

        for record in self:
            record.directory_filecounting = len(record.directory_file_ids)


    # ---------------------- FIELD METHODS AND EVENTS -------------------------

    def _domain_for_training_unit_ids(self):
        """ Compute the domain for the training units, this restrict
        allowed units to those are related with selected modules.
        """

        ids = self.training_module_ids.mapped('training_unit_ids').ids

        return [('id', 'in', ids) if ids else ('id', '=', -1)]


    @api.onchange('directory')
    def _onchange_directory(self):
        """ Onchange event for general_public_access field
        """

        self._reload_single_directory()


    @api.onchange('training_module_ids')
    def _training_module_ids(self):
        """ training_module_ids change event. Update the trainint unit
        list and domain
        """

        #STEP 1: Update the unit set according to the selected modules
        utdel = self._get_units_to_remove()
        utadd = self._get_units_to_add()
        self.training_unit_ids = self.training_unit_ids - utdel +utadd

        #STEP 1: Return new domain to restrict units within selected modules
        return {'domain': {'training_unit_ids': self._domain_for_training_unit_ids()}}


    # ------------------------- AUXLIARY METHODS ------------------------------

    def _get_units_to_remove(self):
        """ Computes which units will be removed from list. This list
        changes when the list of training modules changes before.
        """

        module_ids = self.training_module_ids.ids
        return self.training_unit_ids.filtered(
            lambda item: item.training_module_id.id not in module_ids)


    def _get_units_to_add(self):
        """ Computes which units will be added to list. This list
        changes when the list of training modules changes before.
        """

        unit_ids = self.training_unit_ids
        module_set = self.training_module_ids.filtered(
            lambda item: item.training_unit_ids and \
                         not item.training_unit_ids & unit_ids)

        return module_set.mapped('training_unit_ids')


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

                    if  re.search('^[^~_.]', rel_path):
                        filenames.append(
                            (0, 0, {
                                'name': rel_path,
                                'training_resource_id': record.id
                                }
                            )
                        )

                record.directory_file_ids = filenames

    @staticmethod
    def _zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path): # pylint: disable=locally-disabled, W0612
            for file in files:
                relpath = os.path.relpath(root, path)
                relfile = os.path.join(relpath, file)
                _logger.debug(u'### Zipping %s', relfile)
                ziph.write(os.path.join(root, file), relfile)


    # --------------------------- PUBLIC METHODS ------------------------------

    @api.multi
    def reload_directory(self):
        """ Reload directory filenames
        """

        for record in self:
            record._reload_single_directory() # pylint: disable=locally-disabled, W0212


    @api.multi
    def download_directory(self):
        """ Download related directory as a zip file. This method will be
        called by the Download button in VIEW

        Todo: Reads and writes in external folders, all the behavior should
        be inside a try...except block
        """

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
            _logger.debug(u'zip size: %s', len(datas))
            attach_obj = self.env['ir.attachment']
            attach_obj.create({'name': zipname,
                               'datas': datas,
                               'datas_fname': zipname,
                               'res_model': self._name,
                               'res_id': self.id})


