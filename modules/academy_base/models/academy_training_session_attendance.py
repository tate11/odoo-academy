# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AcademyTrainingSessionAttendance(models.Model):
    """ Student who have participated in the session

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.session.attendance'
    _description = u'Academy training session attendance'

    _rec_name = 'student_id'
    _order = 'student_id ASC'

    academy_training_session_id = fields.Many2one(
        string='Training session',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Choose the related training session',
        comodel_name='academy.training.session',
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
        help='Choose an student',
        comodel_name='res.partner',
        domain=[('is_student', '=', True)],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    start = fields.Datetime(
        string='Start',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help='Choose the start date'
    )

    end = fields.Datetime(
        string='End',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help='Choose the start date'
    )

    description = fields.Text(
        string='Notes',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Enter new note',
        translate=True
    )
