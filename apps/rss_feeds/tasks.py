import feedparser
from rest_framework import status

from config.celery import app
from apps.rss_feeds.models import Feed, FeedItem


@app.task(bind=True)
def update_rss_feeds(self, *args, **kwargs):
    feeds = Feed.objects.all()
    for feed in feeds:
        rss_feed = feedparser.parse(feed.link, modified=feed.rss_server_last_updated)
        if rss_feed.status == status.HTTP_200_OK:
            feed.rss_server_last_updated = rss_feed.updated
            feed.save()
            for entry in rss_feed.entries:
                feed_item = FeedItem.objects.get(
                    item_id=entry.id,
                    feed=feed
                )
                if feed_item.rss_server_last_updated != entry.updated:
                    feed_item.rss_server_last_updated = entry.last_updated
                    feed_item.title = entry.title
                    feed_item.description = entry.description
                    feed_item.save()
