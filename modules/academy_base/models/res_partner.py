# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class ResPartner(models.Model):
    """ The summary line for a class docstring should fit on one line.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'res.partner'
    _inherit = 'res.partner'

    is_student = fields.Boolean(
        string='Is student',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Is an student'
    )

    # training_action_enrolment_ids = fields.One2many(
    #     string='Training actions',
    #     required=False,
    #     readonly=False,
    #     index=False,
    #     default=None,
    #     help=False,
    #     comodel_name='academy.training.action.enrolment',
    #     inverse_name='res_partner_id',
    #     domain=[],
    #     context={},
    #     auto_join=False,
    #     limit=None
    # )
