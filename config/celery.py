import os

from django.conf import settings

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

broker_url = 'amqp://{}:{}@{}:{}/{}'.format(
    settings.RABBIT_USER, settings.RABBIT_PASS, settings.RABBIT_HOST,
    settings.RABBIT_PORT, settings.RABBIT_VHOST
)

app = Celery(
    'rss_scraper',
    broker=broker_url,
    task_serializer='json',
    result_serializer='json',
    accept_content=['application/json']
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(packages=['apps.rss_feeds'])
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'apps.rss_feeds.tasks.update_rss_feeds',
        'schedule': crontab(),
    }
}
