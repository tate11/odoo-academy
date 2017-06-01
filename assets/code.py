clear()

from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
import pytz

print obj.env.context

record = obj.browse(4)
start = datetime.strptime(record.start, DEFAULT_SERVER_DATETIME_FORMAT)
end = datetime.strptime(record.end, DEFAULT_SERVER_DATETIME_FORMAT)

now = datetime.now().replace(tzinfo=pytz.timezone(obj.env.context['tz']))
checkpoint = now.replace(hour=22, minute=0, second=0, microsecond=0)

tomorrow = now + timedelta(days=1)
if now < checkpoint:
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

print '\nstart:', start, '\nend:', end, '\nnow:', now, '\ncheckpoint:', checkpoint, '\ntomorrow:', tomorrow

if end < now:
    print 'ended'
elif start < tomorrow:
    print 'following'
