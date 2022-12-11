import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

app = Celery('mailing')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(timezone='Europe/Moscow')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-stat-every-day': {
        'task': 'mailapp.tasks.send_stat_every_day',
        'schedule': crontab(0, 0, day_of_week='0-6')
    }
}
