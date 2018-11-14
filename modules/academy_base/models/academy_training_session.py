# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Academy Training Session

This module contains the academy.training.session an unique Odoo model
which contains all Academy Training Session attributes and behavior.

This model is the representation of the real life training session. One
session has some related resources and a linked list of students who have
attended.

In addition, training you can designate the modules or units which have
been imparted in it.

Classes:
    AcademyTrainingSession: This is the unique model class in this module
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
from openerp.exceptions import ValidationError


# pylint: disable=locally-disabled, C0103
_logger = getLogger(__name__)



# pylint: disable=locally-disabled, R0903
class AcademyTrainingSession(models.Model):
    """ This model is the representation of the real life training session. One
session has some related resources and a linked list of students who have
attended.

    Fields:
      name (Char)       : Human readable name which will identify each record
      description (Text): Something about the record or other information witch
      has not an specific defined field to store it.
      active (Boolean)  : Checked do the record will be found by search and
      browse model methods, unchecked hides the record.

    """


    _name = 'academy.training.session'
    _description = u'Academy Training Session'

    _rec_name = 'name'
    _order = 'name ASC'

    # pylint: disable=locally-disabled, W0212
    name = fields.Char(
        string='Code',
        required=True,
        readonly=False,
        index=True,
        default=lambda self: self._default_name(),
        help='Enter new name',
        size=12,
        translate=True,
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Enter new description',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help='Enables/disables the record'
    )

    training_action_id = fields.Many2one(
        string='Training action',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.action',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    date_start = fields.Datetime(
        string='Start date/time',
        required=True,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help='Start session date/time'
    )

    # date_start = fields.Date(
    #     string='Date start',
    #     required=False,
    #     readonly=False,
    #     index=False,
    #     default=None,
    #     help=False
    # )

    date_delay = fields.Float(
        string='Date delay',
        required=True,
        readonly=False,
        index=False,
        default=2.0,
        digits=(16, 2),
        help="Time length of the session"
    )

    # -------------------------------------------------------------------------


    @api.model
    def _default_name(self):
        """ Get next value for sequence
        """

        seqxid = 'academy_base.ir_sequence_academy_session'
        seqobj = self.env.ref(seqxid)

        result = seqobj.next_by_id()

        return result

