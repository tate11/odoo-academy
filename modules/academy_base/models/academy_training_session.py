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
        default=True,
        help='Enables/disables the record'
    )

    start = fields.Datetime(
        string='Start',
        required=False,
        readonly=False,
        index=False,
        default=fields.datetime.now(),
        help='Date and time session starts'
    )

    stop = fields.Datetime(
        string='Stop',
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
        compute='_compute_hours',
    )

    unitcounting = fields.Integer(
        string='Units',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Units covered in session',
        compute='_compute_unitcounting',
    )

    studentcounting = fields.Integer(
        string='Students',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Students who have attended this session',
        compute='_compute_studentcounting',
    )

    resourcecounting = fields.Integer(
        string='Resources',
        required=False,
        readonly=True,
        index=False,
        default=0,
        help='Number of resources used in session',
        compute='_compute_resourcecounting',
    )



    @api.multi
    @api.depends('itemisation_ids')
    def _compute_unitcounting(self):
        for record in self:
            record.unitcounting = len(record.itemisation_ids)

    @api.multi
    @api.depends('attendance_ids')
    def _compute_studentcounting(self):
        for record in self:
            record.studentcounting = len(record.attendance_ids)

    @api.multi
    @api.depends('academy_training_resource_ids')
    def _compute_resourcecounting(self):
        for record in self:
            record.resourcecounting = len(record.academy_training_resource_ids)

    @api.multi
    @api.depends('start', 'stop')
    def _compute_hours(self):
        """ Computes hours between start and stop times """
        for record in self:
            start = datetime.strptime(record.start, DEFAULT_SERVER_DATETIME_FORMAT)
            stop = datetime.strptime(record.stop, DEFAULT_SERVER_DATETIME_FORMAT)
            record.hours = (stop - start).seconds / 3600


    @api.constrains('stop')
    def _check_stop(self):
        """ Ensures stop field value is greater then start value """
        for record in self:
            if record.stop <= record.start:
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

    @staticmethod
    def _get_duration(start, stop):
        """ Get the duration value between the 2 given dates. This method will
        be used to compute duration field value in all day appointments.
        """

        if start and stop:
            diff = fields.Datetime.from_string(stop) - fields.Datetime.from_string(start)
            if diff:
                duration = float(diff.days) * 24 + (float(diff.seconds) / 3600)
                return round(duration, 2)

            return 0.0

    @api.multi
    def update_status(self):

        sess_domain = [('id', '>', 1)]
        sess_obj = self.env['academy.training.session']
        sess_set = sess_obj.search(sess_domain)

        today = date.today()
        tomorrow = today + timedelta(days=1)


        for record in sess_set:
            start = record._ctx_timestamp('start').date()
            stop = record._ctx_timestamp('stop').date()

            if stop < today:
                record.status = 'finished'
            elif start < tomorrow:
                record.status = 'current'
            elif start == tomorrow:
                record.status = 'upcoming'
            else:
                record.status = 'expected'

        return True



