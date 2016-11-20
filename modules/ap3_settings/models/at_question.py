# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0212,E0611,C0103,R0903,C0111,F0401
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from __future__ import division

from openerp import models, api
from logging import getLogger
from re import search

_logger = getLogger(__name__)



class AtQuestion(models.Model):
    """ Extends at.question model to use it in townhall reports

    """
    _inherit = ['at.question']

    @api.multi
    def townhall_file(self):
        """ Get filename to use in townhall report
        """
        result = u''
        for record in self:
            if record.preamble:
                matches = search(r'[a-zA-Z0-9-_]+\.[A-Za-z]{1,3}(?!\w)', record.preamble)
                if matches:
                    result += matches.group()

        return result
