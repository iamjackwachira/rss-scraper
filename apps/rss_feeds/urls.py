from django.urls import include, path

from rest_framework_nested import routers

from . import views

app_name = "rss_feeds"

router = routers.SimpleRouter()
router.register(r'feeds', views.FeedViewSet, 'feed')
router.register(r'feed-items', views.FeedItemViewSet, 'feed-items')

details_router = routers.NestedSimpleRouter(router, r'feeds', lookup='feed')
details_router.register(r'items', views.FeedItemViewSet, 'items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(details_router.urls)),
]
