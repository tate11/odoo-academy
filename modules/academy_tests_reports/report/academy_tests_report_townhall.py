# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Academy Test Report Townhall

This module contains the academy.test.report.townhall an unique Odoo model
which contains all Academy Test Report Townhall attributes and behavior.

This model is the representation of the real life academy test report townhall

Classes:
    AcademyTestReportTownhall: This is the unique model class in this module
    and it defines an Odoo model with all its attributes and related behavior.

    Inside this class can be, in order, the following attributes and methods:
    * Object attributes like name, description, inheritance, etc.
    * Entity fields with the full definition
    * Computed fields and required computation methods
    * Events (@api.onchange) and other field required methods like computed
    domain, defaul values, etc...
    * Overloaded object methods, like create, write, copy, etc.
    * Public object methods will be called from outside
    * Private auxiliary methods not related with the model fields, they will
    be called from other class methods


Todo:
    * Complete the model attributes and behavior

"""


from logging import getLogger

# pylint: disable=locally-disabled, E0401
from openerp import models, fields, api
from openerp.tools.translate import _


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTestReportTownhall(models.AbstractModel):
    """ This model is the representation of the academy test report townhall

    Fields:
      name (Char)       : Human readable name which will identify each record
      description (Text): Something about the record or other information witch
      has not an specific defined field to store it.
      active (Boolean)  : Checked do the record will be found by search and
      browse model methods, unchecked hides the record.

    """


    _name = 'academy.test.report.townhall'
    _description = u'Academy Test Report Townhall'


    @api.model
    def get_report_values(self, docids, data=None):
        print('Hola')
        super(AcademyTestReportTownhall, self).get_report_values(docids, data)
