import logging
import feedparser
from django.conf import settings
from rest_framework import status

from config.celery import app
from apps.rss_feeds.models import Feed, FeedItem

logger = logging.getLogger(__name__)


@app.task(bind=True, default_retry_delay=settings.RABBIT_RETRY_DELAY, max_retries=settings.RABBIT_MAX_RETRIES)
def update_rss_feeds(self, *args, **kwargs):
    feeds = Feed.objects.all()
    for feed in feeds:
        rss_feed = feedparser.parse(feed.link, modified=feed.rss_server_last_updated)
        if status.is_success(rss_feed.status):
            feed.rss_server_last_updated = rss_feed.updated
            feed.save()
            for entry in rss_feed.entries:
                feed_item = FeedItem.objects.get(
                    item_id=entry.id,
                    feed=feed
                )
                if feed_item.rss_server_last_updated != entry.updated:
                    feed_item.rss_server_last_updated = entry.updated
                    feed_item.title = entry.title
                    feed_item.description = entry.description
                    feed_item.save()
        elif status.is_client_error(rss_feed.status) or status.is_server_error(rss_feed.status):
            try:
                raise self.retry()
            except self.MaxRetriesExceededError as e:
                logger.error(e)
                feed.update_success = False
                feed.save()
