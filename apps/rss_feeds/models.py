from django.contrib.auth.models import User
from django.db import models

from apps.core.models import BaseModel


class BaseFeed(BaseModel):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    description = models.TextField()

    class Meta:
        abstract = True


class Feed(BaseFeed):
    """ RSS Feeds """

    language = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='feeds')

    class Meta:
        ordering = ('modified_on',)

    def __str__(self):
        return f'{self.title}'


class FeedItem(BaseFeed):
    """ Feed Items contained in a Feed """

    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name='feed_items')
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Feed Item'
        verbose_name_plural = 'Feed Items'
        ordering = ('modified_on',)

    def __str__(self):
        return f'{self.title}'
