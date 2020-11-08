import logging

from django.conf import settings

from config.celery import app
from apps.rss_feeds.models import Feed

from .exceptions import RssFeedUpdateError

logger = logging.getLogger(__name__)


@app.task(bind=True, default_retry_delay=settings.RABBIT_RETRY_DELAY, max_retries=settings.RABBIT_MAX_RETRIES)
def update_rss_feeds(self, *args, **kwargs):
    feeds = Feed.objects.all()
    for feed in feeds:
        try:
            feed.update_feed_items()
        except RssFeedUpdateError:
            try:
                raise self.retry()
            except self.MaxRetriesExceededError as e:
                logger.error(e)
                feed.update_success = False
                feed.save()
