from rest_framework import serializers

from .models import FeedFollow


class FeedFollowSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='feed.title')
    description = serializers.ReadOnlyField(source='feed.description')
    link = serializers.ReadOnlyField(source='feed.link')
    pub_date = serializers.ReadOnlyField(source='feed.pub_date')

    class Meta:
        model = FeedFollow
        fields = ('title', 'description', 'link', 'pub_date')
