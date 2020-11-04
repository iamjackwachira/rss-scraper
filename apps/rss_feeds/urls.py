from django.conf.urls import include, url

from rest_framework import routers
from . import views

app_name = "rss_feeds"

router = routers.SimpleRouter()
router.register(r'', views.FeedFollowViewSet, 'feeds-follow')

urlpatterns = [
    url(r'^', include(router.urls))
]
