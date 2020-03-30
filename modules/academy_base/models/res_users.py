# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Res Users

This module extends the res.users to link with training resources
"""


from logging import getLogger

# pylint: disable=locally-disabled, E0401
from odoo import models, fields


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class ResUsers(models.Model):
    """ This model is the representation of the res users

    Fields:
      training_resource_ids: related resources
    """


    _name = 'res.users'
    _inherit = ['res.users']


    training_resource_ids = fields.One2many(
        string='Training resources',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Choose the training resources which he/she must update',
        comodel_name='academy.training.resource',
        inverse_name='updater_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

