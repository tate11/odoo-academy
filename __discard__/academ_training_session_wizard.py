 start_date = fields.Date(
        string='Start date',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: fields.Date.context_today(self), # pylint: disable=locally-disabled, W0108
        help='Start date'
    )

    stop_date = fields.Date(
        string='Stop date',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: fields.Date.context_today(self), # pylint: disable=locally-disabled, W0108
        help='End date'
    )

    start_time = fields.Float(
        string='Start time',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_start_time(), # pylint: disable=locally-disabled, W0212
        digits=(16, 2),
        help='Start time'
    )

    duration = fields.Float(
        string='Duration',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_duration(), # pylint: disable=locally-disabled, W0212
        digits=(16, 2),
        help='Duration'
    )

    allday = fields.Boolean(
        string='Allday',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='All day'
    )

    interval = fields.Integer(
        string='Repeat every',
        required=False,
        readonly=False,
        index=False,
        default=1,
        help='Repeat every (Days/Week/Month/Year)'
    )
