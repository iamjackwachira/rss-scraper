import json
import pytest

from django.urls import reverse
from box import Box
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from factories.models import FeedFactory, UserFactory
from apps.rss_feeds.models import FeedItem


@pytest.mark.django_db
class TestFeeds(APITestCase):
    def setUp(self):
        user = UserFactory.create()
        self.feeds = FeedFactory.create_batch(3, user=user)
        self.client.force_authenticate(user=user)
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
                }
            ],
            'bozo': 0,
            'status': 200,
            'updated': 'Sun, 08 Nov 2020 10:39:58 GMT',
            'modified': 'Sun, 08 Nov 2020 10:39:58 GMT'
        }

    def test_get_feeds(self):
        url = reverse('rss_feeds:feed-list')
        response = self.client.get(url)
        json_data = json.loads(json.dumps(response.data))
        assert response.status_code == status.HTTP_200_OK
        assert len(json_data) == 3

    def test_get_one_feed(self):
        url = reverse('rss_feeds:feed-detail', kwargs={'pk': self.feeds[0].pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('id') == self.feeds[0].id

    @patch('apps.rss_feeds.views.feedparser')
    def test_follow_feed(self, feedparser):
        feedparser.parse.return_value = Box(self.rss_feed)
        url = reverse('rss_feeds:feed-list')
        response = self.client.post(url, data={'url': 'http://www.nu.nl/rss/Algemeen'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('title') == 'Feed1'

    def test_unfollow_feed(self):
        url = reverse('rss_feeds:feed-detail', kwargs={'pk': self.feeds[0].pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = self.client.get(reverse('rss_feeds:feed-list'))
        json_data = json.loads(json.dumps(response.data))
        assert len(json_data) == 2

    @patch('apps.rss_feeds.models.feedparser')
    def test_force_feed_update(self, feedparser):
        feedparser.parse.return_value = Box(self.rss_feed)
        url = reverse('rss_feeds:feed-force-feed-update', kwargs={'pk': self.feeds[0].pk})
        response = self.client.post(url, data={})
        assert response.status_code == status.HTTP_200_OK
        feed_items = FeedItem.objects.all()
        assert len(feed_items) == 1
        assert feed_items[0].title == 'Entry1'
