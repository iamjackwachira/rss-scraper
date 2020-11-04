from django.contrib import admin

from .models import Feed, FeedItem, FeedFollow


class FeedAdmin(admin.ModelAdmin):
    list_display = ("title", "pub_date", "language")
    display = "Feed"


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ("feed", "title", "pub_date", "is_permalink")
    display = "Feed Item"


class FeedFollowAdmin(admin.ModelAdmin):
    list_display = ("feed", "user", "created_on")
    display = "Feed Follow"


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
admin.site.register(FeedFollow, FeedFollowAdmin)
