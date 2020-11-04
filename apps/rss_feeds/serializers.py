from rest_framework import serializers

from .models import FeedFollow


class FeedFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedFollow
        fields = ('__all__')
