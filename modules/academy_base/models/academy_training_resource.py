#pylint: disable=I0011,W0212,C0111,F0401,R0903
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api



class AcademyTriningResource(models.Model):
    """ Resource will be used in a training unit or session

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.resource'
    _description = u'Academy trining resource'

    _rec_name = 'name'
    _order = 'name ASC'


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

    academy_training_session_ids = fields.Many2many(
        string='Training sessions',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.session',
        # relation='academy_training_activity_this_model_rel',
        # column1='academy_training_activity_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None
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
        help='Resources stored in Odoo database',
        comodel_name='ir.attachment',
        # relation='model_name_this_model_rel',
        # column1='model_name_id',
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


    @api.multi
    def reload_directory(self):
        """ Reload directory filenames
        """

        import os
        import re

        for record in self:
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




# import subprocess
# p = subprocess.Popen([r'C:\Program Files\Ghostgum\gsview\gsprint.exe', '-printer', r'PDFCreator', '-copies', '10', '
# stdout, stderr = p.communicate()
# print stdout
# print stderr
