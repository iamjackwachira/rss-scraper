from rest_framework import serializers

from .models import Feed, FeedItem


class FollowFeedSerializer(serializers.Serializer):
    url = serializers.URLField()


class FeedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedItem
        fields = ('__all__')


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        exclude = ('user',)
