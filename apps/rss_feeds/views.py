from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import FeedSerializer, FeedItemSerializer, FollowFeedSerializer
from .models import FeedFollow, FeedItem


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeedFollow.objects.all()
    ordering_fields = ['created_on']
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ['follow']:
            return FollowFeedSerializer
        return FeedSerializer

    def list(self, request):
        queryset = self.get_queryset()
        feeds = queryset.filter(user=request.user)
        serializer = self.get_serializer(feeds, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None, **kwargs):
        feed = self.get_object()
        follow, created = FeedFollow.objects.get_or_create(
            feed__id=feed.feed_id, user__id=feed.user_id)
        serializer = self.get_serializer(follow)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def unfollow(self, request, pk=None, **kwargs):
        feed = self.get_object()
        feed_follow = FeedFollow.objects.get(
            feed__id=feed.feed_id, user__id=feed.user_id)
        feed_follow.delete()
        serializer = self.get_serializer(feed_follow)
        return Response(serializer.data)


class FeedItemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        return FeedItem.objects.filter(feed_id=self.kwargs['feed_pk'])
