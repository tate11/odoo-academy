# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyTrainingSessionItemisation(models.Model):
    """ List of training units imparted in a training session.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.session.itemisation'
    _description = u'Academy training session itemisation'

    _rec_name = 'hours'
    _order = 'sequence ASC'

    academy_training_unit_id = fields.Many2one(
        string='Training unit',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Training unit imparted in session',
        comodel_name='academy.training.unit',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    academy_training_session_id = fields.Many2one(
        string='Training session',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Training session to which this itemisation is related',
        comodel_name='academy.training.session',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    sequence = fields.Integer(
        string='Sequence',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help="Choose unit order"
    )

    hours = fields.Float(
        string='Hours',
        required=True,
        readonly=False,
        index=False,
        default=1.0,
        digits=(16, 2),
        help='Time (hours) dedicated to each one of the training activities in session'
    )

