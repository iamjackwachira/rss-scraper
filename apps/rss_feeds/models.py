import feedparser

from django.contrib.auth.models import User
from django.db import models

from rest_framework import status
from .exceptions import RssFeedUpdateError


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    description = models.TextField()
    rss_server_last_updated = models.CharField(max_length=100,
                                               help_text="Last updated date/time from RSS server")

    class Meta:
        abstract = True


class Feed(BaseModel):
    """ RSS Feeds """

    language = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feeds')
    update_success = models.BooleanField(default=True)

    class Meta:
        ordering = ('-modified_on',)

    def __str__(self):
        return f'{self.title}'

    def update_feed_items(self, force=False):
        if force:
            rss_feed = feedparser.parse(self.link)
        else:
            rss_feed = feedparser.parse(self.link, modified=self.rss_server_last_updated)
        if rss_feed.bozo:
            bozo_exception = rss_feed.bozo_exception.getMessage()
            raise RssFeedUpdateError(bozo_exception)
        if status.is_success(rss_feed.status):
            self.rss_server_last_updated = rss_feed.updated
            self.save()
            for entry in rss_feed.entries:
                try:
                    feed_item = FeedItem.objects.get(
                        item_id=entry.id,
                        feed=self)
                    if feed_item.rss_server_last_updated != entry.updated:
                        feed_item.rss_server_last_updated = entry.updated
                        feed_item.title = entry.title
                        feed_item.description = entry.description
                        feed_item.save()
                except FeedItem.DoesNotExist:
                    FeedItem.objects.create(
                        item_id=entry.id,
                        feed=self,
                        rss_server_last_updated=entry.updated,
                        title=entry.title,
                        description=entry.description
                    )
        return self


class FeedItem(BaseModel):
    """ Feed Items contained in a Feed """

    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name='feed_items')
    read = models.BooleanField(default=False)
    item_id = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Feed Item'
        verbose_name_plural = 'Feed Items'
        ordering = ('-modified_on',)
        unique_together = ('feed', 'item_id')

    def __str__(self):
        return f'{self.title}'
