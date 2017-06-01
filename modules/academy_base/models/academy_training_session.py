#pylint: disable=I0011,W0212,C0111,F0401,R0903
# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from openerp.tools.translate import _
from logging import getLogger
from openerp.exceptions import ValidationError
from datetime import datetime, timedelta, date


_logger = getLogger(__name__)



class AcademyTrainingSession(models.Model):
    """ Information about training sessions

    Fields:
      name (Char): Human readable name which will identify each record.

    """
    STATUS_LIST = [
        ('unestablished', 'Unestablished'),
        ('archived', 'Archived'),
        ('finished', 'Finished'),
        ('current', 'Current'),
        ('upcoming', 'Upcoming '),
        ('expected', 'Expected')
    ]

    FOLDED_STATUS = [
        'unestablished'
        'archived',
        'finished'
    ]

    _name = 'academy.training.session'
    _description = u'Academy training session'

    _rec_name = 'name'
    _order = 'name ASC'

    @api.model
    def _status_groups(self, present_ids, domain, **kwargs):
        #pylint: disable=I0011,W0613
        folded = {key: (key in self.FOLDED_STATUS) for key, _ in self.STATUS_LIST}
        # Need to copy self.STATES list before returning it,
        # because odoo modifies the list it gets,
        # emptying it in the process. Bad odoo!
        return self.STATUS_LIST[:], folded

    _group_by_full = {
        'status': _status_groups
    }

    @api.multi
    def _read_group_fill_results(self, domain, groupby,
                                 remaining_groupbys, aggregated_fields,
                                 count_field, read_group_result,
                                 read_group_order=None):
        #pylint: disable=I0011,R0913
        """
        The method seems to support grouping using m2o fields only,
        while we want to group by a simple status field.
        Hence the code below - it replaces simple status values
        with (value, name) tuples.
        """
        # if groupby == 'status':
        #     status_dict = dict(self.STATUS_LIST)
        #     for result in read_group_result:
        #         status = result['status']
        #         result['status'] = (status, status_dict.get(status))

        # print read_group_result, read_group_order

        new_read_group_result = []
        in_list = [item['status'] for item in read_group_result]

        for item in self.STATUS_LIST:
            if item[0] in in_list:
                data = read_group_result[in_list.index(item[0])]

                if item[0] in self.FOLDED_STATUS:
                    data['__fold'] = True

                new_read_group_result.append(
                    data
                )

            else:
                new_read_group_result.append({
                    'status': (item[0], item[1]),
                    '__domain': [(u'status', '=', item[0])],
                    'status_count': 0L,
                    '__fold': True
                })

        result = super(AcademyTrainingSession, self)._read_group_fill_results(
            domain, groupby, remaining_groupbys, aggregated_fields,
            count_field, new_read_group_result, read_group_order
        )

        return result

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
        default='Enables/disables the record',
        help=False
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

    academy_training_action_id = fields.Many2one(
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

    itemisation_ids = fields.One2many(
        string='Itemisation',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.session.itemisation',
        inverse_name='academy_training_session_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    academy_training_resource_ids = fields.Many2many(
        string='Training resource',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help=False,
        comodel_name='academy.training.resource',
        # relation='academy_training_resource_this_model_rel',
        # column1='academy_training_resource_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    attendance_ids = fields.One2many(
        string='Attendance',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Register new student in session',
        comodel_name='academy.training.session.attendance',
        inverse_name='academy_training_session_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    hours = fields.Float(
        string='Hours',
        required=False,
        readonly=True,
        index=False,
        default=0.0,
        digits=(16, 2),
        help='Time lenght in hours',
        compute=lambda self: self._compute_hours()
    )

    @api.multi
    @api.depends('hours')
    def _compute_hours(self):
        """ Computes hours between start and end times """
        for record in self:
            start = datetime.strptime(record.start, DEFAULT_SERVER_DATETIME_FORMAT)
            end = datetime.strptime(record.end, DEFAULT_SERVER_DATETIME_FORMAT)
            record.hours = (end - start).seconds / 3600


    @api.constrains('end')
    def _check_end(self):
        """ Ensures end field value is greater then start value """
        for record in self:
            if record.end <= record.start:
                raise ValidationError("End date must be greater then start date")


    status = fields.Selection(
        string='Status',
        required=True,
        readonly=False,
        index=False,
        default='unestablished',
        help=False,
        selection=STATUS_LIST
    )

    @api.multi
    def _ctx_timestamp(self, field_name):
        """ Converts Odoo field timestamp to python timestap with context """

        self.ensure_one()

        time_str = self.mapped(field_name)[0]

        return fields.Datetime.context_timestamp(
            self, fields.Datetime.from_string(time_str)
        )


    @api.multi
    def update_status(self):

        sess_domain = [('id', '>', 1)]
        sess_obj = self.env['academy.training.session']
        sess_set = sess_obj.search(sess_domain)

        today = date.today()
        tomorrow = today + timedelta(days=1)


        for record in sess_set:
            start = record._ctx_timestamp('start').date()
            end = record._ctx_timestamp('end').date()

            if end < today:
                record.status = 'finished'
            elif start < tomorrow:
                record.status = 'current'
            elif start == tomorrow:
                record.status = 'upcoming'
            else:
                record.status = 'expected'

        return True



