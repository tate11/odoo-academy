# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0212,E0611,C0103,R0903,C0111,F0401
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from logging import getLogger


_logger = getLogger(__name__)


class AtQuestionImpugnment(models.Model):
    """ Question impugnment

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'at.question.impugnment'
    _description = u' Question impugnment'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Title',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Short impugnment description',
        size=50,
        translate=True
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Long impugnment description',
        translate=True
    )

    at_question_id = fields.Many2one(
        string='Question',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Question related with this impugnment',
        comodel_name='at.question',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help=('If the active field is set to false, it will allow you to '
              'hide record without removing it.')
    )
