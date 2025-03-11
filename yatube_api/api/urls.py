from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AuthToken, CommentViewSet, GroupViewSet, PostViewSet
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'groups', GroupViewSet, basename='group')
router.register(
    r'posts/(?P<post_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('api-token-auth/', AuthToken.as_view(), name='api_token_auth'),
    path('', include(router.urls)),
]
