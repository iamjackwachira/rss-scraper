import feedparser

from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .exceptions import RssFeedUpdateError
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
        feed_url = serializer.validated_data['url']
        rss_feed = feedparser.parse(feed_url)
        if rss_feed.bozo:
            bozo_exception = rss_feed.bozo_exception.getMessage()
            return Response({"message": f"RSS feed could not be processed: {bozo_exception}"},
                            status=status.HTTP_400_BAD_REQUEST)
        feed = Feed.objects.create(
            title=rss_feed.feed.title,
            link=feed_url,
            description=rss_feed.feed.description,
            language=rss_feed.feed.language,
            user=request.user,
            rss_server_last_updated=rss_feed.modified
        )
        for entry in rss_feed.entries:
            FeedItem.objects.create(
                item_id=entry.id,
                rss_server_last_updated=entry.updated,
                title=entry.title,
                link=entry.link,
                description=entry.description,
                feed=feed
            )
        headers = self.get_success_headers(feed)
        serializer = self.get_serializer(feed)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def force_feed_update(self, request, pk=None, **kwargs):
        feed = self.get_object()
        try:
            feed.update_feed_items(force=True)
        except RssFeedUpdateError as e:
            feed.update_success = False
            feed.save()
            return Response({"message": f"RSS feeds could not be updated: {e}"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": f"RSS feeds updated successfully"},
                        status=status.HTTP_200_OK)


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
