# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api, api
from odoo.tools.translate import _
from odoo.exceptions import AccessDenied

from logging import getLogger
from datetime import datetime, timedelta

_logger = getLogger(__name__)


class AptPublicTendering(models.Model):
    """ Public tendering information

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'academy.public.tendering.process'
    _description = u'Public tendering'

    _inherit = ['image.mixin', 'mail.thread']

    _rec_name = 'name'
    _order = 'approval DESC'


    STATES = [
        ('0', _('Expected')),
        ('1', _('Approved')),
        ('2', _('Announced')),
        ('3', _('Convened')),
        ('4', _('Finished'))
    ]

    # States that should be folded in Kanban view
    # used by the `state_groups` method
    FOLDED_STATES = [
        'finished',
    ]


    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Name for this academy public tendering',
        size=50,
        translate=True,
        track_visibility='always'
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Something about this academy public tendering',
        translate=True
    )

    active = fields.Boolean(
        string='Active',
        required=False,
        readonly=False,
        index=False,
        default=True,
        help=('If the active field is set to false, it will allow you '
              'to hide record without removing it.'),
        track_visibility='onchange'
    )

    administration_id = fields.Many2one(
        string='Administration',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Choose the administration related with tendering',
        comodel_name='res.partner',
        domain=lambda self: self.administration_id_domain(),
        context={},
        ondelete='cascade',
        auto_join=False,
        track_visibility='always'
    )

    approval = fields.Date(
        string='Approval date',
        required=False,
        readonly=False,
        index=False,
        default=fields.Date.today(),
        help='Choose the approval date',
        track_visibility = 'onchange'
    )

    announcement = fields.Date(
        string='Announcement date',
        required=False,
        readonly=False,
        index=False,
        default=fields.Date.today(),
        help='Choose the Announcement date',
        track_visibility = 'onchange'
    )

    target_date = fields.Date(
        string='Target date',
        required=False,
        readonly=False,
        index=False,
        # default=lambda self: self.default_submissions_deadline()
        help='Choose the last day for training',
        track_visibility='onchange'
    )

    vacancy_position_ids = fields.One2many(
        string='Vacancy positions',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Add offered vacancy positions',
        comodel_name='academy.public.tendering.vacancy.position',
        inverse_name='academy_public_tendering_process_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    ir_atachment_ids = fields.Many2many(
        string='Attachments',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Documents related with the academy public tendering',
        comodel_name='ir.attachment',
        relation='academy_public_tendering_process_ir_attachment_rel',
        column1='tendering_process_id',
        column2='ir_atachment_id',
        domain=[],
        context={},
        limit=None,
        track_visibility='onchange'
    )

    bulletin_board_url = fields.Char(
        string='Bulletin Board',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='URL of the bulletin board',
        size=256,
        translate=True
    )

    official_journal_url = fields.Char(
        string='Official journal',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='URL of the article in the official journal',
        size=256,
        translate=True
    )

    total_of_vacancies = fields.Integer(
        string='Vacancies',
        required=False,
        readonly=True,
        index=False,
        default=0,
        compute='compute_total_of_vacancies',
        help='Set number of vacancies'
    )

    training_action_ids = fields.Many2many(
        string='Training action',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.action',
        relation='academy_training_action_public_tendering_process_rel',
        column1='public_tendering_id',
        column2='training_action_id',
        domain=[],
        context={},
        limit=None,
        track_visibility='onchange'
    )

    state = fields.Selection(
        string='State',
        required=False,
        readonly=False,
        index=False,
        default='expected',
        help=False,
        selection=lambda self: self.STATES
    )


    # ----------------------- AUXILIAR FIELD METHODS --------------------------

    @staticmethod
    def default_submissions_deadline():
        """ Returns the default value for deadline_for_submissions field. This
        must be twenty days after the announcement date.
        """
        return fields.Date.to_string(
            datetime.now() + timedelta(days=20)
        )

    @api.model
    def administration_id_domain(self):
        """ Computes domain for administration_id
        """

        xid = 'academy_public_tendering.res_partner_category_civil_service'
        record = self.env.ref(xid)

        return [
            ('is_company', '=', True),
            ('category_id', '=', record.id)
        ]


    # @api.multi
    @api.depends('vacancy_position_ids')
    def compute_total_of_vacancies(self):
        """ Returns computed value for total_of_vacancies field
        """
        for record in self:
            record.total_of_vacancies = \
                sum(record.vacancy_position_ids.mapped('quantity'))


    # ------------------------- OVERLOADED METHODS ----------------------------


    def _state_updated(self, values):
        minstr = datetime.min.strftime('%Y-%m-%d %H:%M:%S')
        now = datetime.now()

        target_date = values.get('target_date', self.target_date)
        approval = values.get('approval', self.approval)
        announced = values.get('announcement', self.announcement)

        if target_date:
            if fields.Datetime.from_string(target_date) < now:
                values['state'] = self.STATES[4][0]
            else:
                values['state'] = self.STATES[3][0]
        elif announced:
                if fields.Datetime.from_string(announced) <= now:
                    values['state'] = self.STATES[2][0]
                else:
                    values['state'] = self.STATES[1][0]
        elif approval:
            if fields.Datetime.from_string(approval) <= now:
                values['state'] = self.STATES[1][0]
            else:
                values['state'] = self.STATES[0][0]
        else:
            values['state'] = self.STATES[0][0]

        return values


    @api.model
    def create(self, values):
        """ Set right state
        """

        values = self._state_updated(values)
        result = super(AptPublicTendering, self).create(values)

        return result


    # @api.multi
    def write(self, values):
        """ Set right state
        """

        values = self._state_updated(values)
        result = super(AptPublicTendering, self).write(values)

        return result

    @api.model
    def update_states(self):
        if not self.env.is_admin():
            raise AccessDenied()
        for record in self.search([]):
            record.write({})