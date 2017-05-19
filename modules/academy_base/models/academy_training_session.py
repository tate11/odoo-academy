# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from logging import getLogger
from openerp.exceptions import ValidationError


_logger = getLogger(__name__)


class AcademyTrainingSession(models.Model):
    """ Information about training sessions

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.training.session'
    _description = u'Academy training session'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help=False,
        size=50,
        translate=True
    )

    start = fields.Datetime(
        string='Start',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help='Date and time session starts'
    )

    end = fields.Datetime(
        string='End',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help='Date and time session ends'
    )


    @api.constrains('end')
    def _check_end(self):
        """ Ensures end field value is greater then start value """
        for record in self:
            if record.end <= record.start:
                raise ValidationError("End date must be greater then start date")
