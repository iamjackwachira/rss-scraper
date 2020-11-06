from django.conf.urls import include, url

from rest_framework_nested import routers

from . import views

app_name = "rss_feeds"

router = routers.SimpleRouter()
router.register(r'feeds', views.FeedViewSet, 'feed')
router.register(r'feed-items', views.FeedItemViewSet, 'feed-items')

details_router = routers.NestedSimpleRouter(router, r'feeds', lookup='feed')
details_router.register(r'items', views.FeedItemViewSet, 'items')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(details_router.urls)),
]
