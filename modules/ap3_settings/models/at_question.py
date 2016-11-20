# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp.http import route, request, Controller
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AtQuestion(models.Model):
    """ Questions are the academy tests cornerstone. Each one of the questions
    belongs to a single topic but they can belong to more than one question in
    the selected topic.

    Fields:
      name (Char): Human readable name which will identify each record.

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
