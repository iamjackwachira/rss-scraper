from rest_framework import permissions, viewsets
from rest_framework.response import Response

from .serializers import FeedFollowSerializer, FeedItemSerializer
from .models import FeedFollow, FeedItem


class FeedFollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FeedFollowSerializer
    queryset = FeedFollow.objects.all()
    ordering_fields = ['created_on']
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset()
        feeds = queryset.filter(user=request.user)
        serializer = self.get_serializer(feeds, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeedItemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        return FeedItem.objects.filter(feed_id=self.kwargs['feed_pk'])
