from rest_framework import serializers

from .models import FeedFollow, FeedItem


class FeedSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='feed.id')
    title = serializers.ReadOnlyField(source='feed.title')
    description = serializers.ReadOnlyField(source='feed.description')
    url = serializers.ReadOnlyField(source='feed.link')
    pub_date = serializers.ReadOnlyField(source='feed.pub_date')

    class Meta:
        model = FeedFollow
        fields = ('id', 'title', 'description', 'url', 'pub_date')


class FeedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedItem
        fields = ('__all__')


class FollowFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedFollow
        fields = ('__all__')
