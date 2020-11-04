from django.db import models

from core.models import BaseModel


class BaseFeed(BaseModel):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField()

    class Meta:
        abstract = True


class Feed(BaseFeed):
    """
    RSS Feeds
    """
    language = models.CharField(max_length=50)

    class Meta:
        ordering = ('created_on',)

    def __str__(self):
        return f'{self.title}'


class FeedItem(BaseFeed):
    """
    Feed Items contained in a Feed
    """

    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name='feed_items')
    is_permalink = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Feed Item'
        verbose_name_plural = 'Feed Items'

    def __str__(self):
        return f'{self.title}'
