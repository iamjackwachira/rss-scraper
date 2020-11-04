from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from .serializers import FeedFollowSerializer
from .models import FeedFollow


class FeedFollowViewSet(generics.ListAPIView, viewsets.GenericViewSet):
    serializer_class = FeedFollowSerializer
    queryset = FeedFollow.objects.all()
    ordering_fields = ['created_on']
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset()
        feeds = queryset.filter(user=request.user)
        serializer = self.get_serializer(feeds, many=True)
        return Response(serializer.data)
