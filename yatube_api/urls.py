from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('api/', include(router.urls)),
]
