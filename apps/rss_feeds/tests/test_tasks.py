import pytest

from box import Box
from rest_framework.test import APITestCase
from unittest.mock import patch
from pytest import raises
from celery.exceptions import Retry

from factories.models import FeedFactory, UserFactory
from apps.rss_feeds.tasks import update_rss_feeds
from apps.rss_feeds.models import FeedItem


@pytest.mark.django_db
class TestFeeds(APITestCase):
    def setUp(self):
        user = UserFactory.create()
        self.feed = FeedFactory.create(user=user)
        self.client.force_authenticate(user=user)

        def getMessage():
            return "Error"

        self.rss_feed = {
            'feed': {
                'title': 'Feed1',
                'description': 'Description',
                'language': 'en',
                'updated': 'Sun, 08 Nov 2020 10:39:58 GMT'
            },
            'entries': [
                {
                    'id': 1,
                    'title': 'Entry1',
                    'description': 'Entry1 Description',
                    'link': 'https://google.com',
                    'updated': 'Sun, 08 Nov 2020 10:39:58 GMT'
                },
                {
                    'id': 2,
                    'title': 'Entry2',
                    'description': 'Entry2 Description',
                    'link': 'https://website.com',
                    'updated': 'Sun, 08 Nov 2020 10:49:58 GMT'
                }
            ],
            'bozo': 0,
            'bozo_exception': {
                'getMessage': getMessage
            },
            'status': 200,
            'updated': 'Sun, 08 Nov 2020 10:39:58 GMT',
            'modified': 'Sun, 08 Nov 2020 10:39:58 GMT'
        }

    @patch('apps.rss_feeds.models.feedparser')
    def test_update_feeds_success(self, feedparser):
        feedparser.parse.return_value = Box(self.rss_feed)
        update_rss_feeds()
        feedparser.parse.assert_called_with(self.feed.link,
                                            modified=self.feed.rss_server_last_updated.strftime("%Y-%m-%d %H:%M:%S"))
        feed_items = FeedItem.objects.all()
        assert len(feed_items) == 2
        assert feed_items[0].title == 'Entry2'
        assert feed_items[1].title == 'Entry1'

    @patch('apps.rss_feeds.models.feedparser')
    def test_update_feeds_error(self, feedparser):
        rss_feed_error = self.rss_feed.copy()
        rss_feed_error['bozo'] = 1  # Cause error
        feedparser.parse.return_value = Box(rss_feed_error)

        with raises(Retry):
            update_rss_feeds()
            modified = self.feed.rss_server_last_updated.strftime("%Y-%m-%d %H:%M:%S")
            feedparser.parse.assert_called_with(self.feed.link,
                                                modified=modified)
            feed_items = FeedItem.objects.all()
            assert len(feed_items) == 0
            assert self.feed.update_success is False
