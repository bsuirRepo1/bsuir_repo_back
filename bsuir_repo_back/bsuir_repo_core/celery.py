from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bsuir_repo_core.settings')
broker_url = os.getenv('BROKER_URL', 'redis://redis:6379/0')

app = Celery('bsuir_repo_core')
app.conf.broker_url = broker_url
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['bsuir_repo_core'])


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
