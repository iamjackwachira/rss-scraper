from rest_framework import permissions

from .models import FeedItem


class IsFeedOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a
    feed to have access to it.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, FeedItem):
            return obj.feed.user == request.user
        return obj.user == request.user
