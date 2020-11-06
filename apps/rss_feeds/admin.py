from django.contrib import admin

from .models import Feed, FeedItem


class FeedAdmin(admin.ModelAdmin):
    list_display = ("title", "pub_date", "language")
    display = "Feed"


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ("feed", "title", "pub_date", "is_permalink")
    display = "Feed Item"


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
