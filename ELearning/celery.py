import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ELearning.settings')

app = Celery('ELearning')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()