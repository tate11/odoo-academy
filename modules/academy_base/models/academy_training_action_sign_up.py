# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyTrainingActionSignUp(models.Model):
    """ Relation between students and training actions

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.action.sign_up'
    _description = u'academy_training_action_sign_up'

    _rec_name = 'date'
    _order = 'date ASC'


    academy_training_action_id = fields.Many2one(
        string='Training action',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Choose the training action in which student will be enrolled',
        comodel_name='academy.training.action',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    student_id = fields.Many2one(
        string='Student',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Choose a student',
        comodel_name='res.partner',
        domain=[('is_student', '=', True)],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    date = fields.Date(
        string='Date',
        required=True,
        readonly=False,
        index=False,
        default=fields.Date.today(),
        help='Date in which student sign up'
    )

