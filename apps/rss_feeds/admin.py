from django.contrib import admin

from .models import Feed, FeedItem


class FeedAdmin(admin.ModelAdmin):
    list_display = ("title", "language")
    display = "Feed"


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ("feed", "title")
    display = "Feed Item"


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
