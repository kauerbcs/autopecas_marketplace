from __future__ import absolute_import

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autopecas_marketplace.settings')

app = Celery('autopecas_marketplace')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'restock-parts-daily': {
        'task': 'marketplace.tasks.restock_parts',
        'schedule': crontab(hour=0, minute=0),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
