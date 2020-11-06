from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import FeedItem, Feed
from .permissions import IsFeedOwner
from .serializers import FeedSerializer, FeedItemSerializer, FollowFeedSerializer


class FeedViewSet(viewsets.ModelViewSet):
    ordering_fields = ['created_on']
    permission_classes = [IsFeedOwner & permissions.IsAuthenticated]
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = FollowFeedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Logic for fetching rss feed ..
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FeedItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsFeedOwner & permissions.IsAuthenticated]
    serializer_class = FeedItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['read']

    def get_queryset(self):
        if 'feed_pk' in self.kwargs:
            return FeedItem.objects.filter(feed_id=self.kwargs['feed_pk'], feed__user=self.request.user)
        return FeedItem.objects.filter(feed__user=self.request.user)

    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None, **kwargs):
        feed_item = self.get_object()
        feed_item.read = True
        feed_item.save()
        serializer = self.get_serializer(feed_item)
        return Response(serializer.data)
