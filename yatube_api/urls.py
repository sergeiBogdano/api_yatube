from django.urls import include

from api.views import CommentViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('api/v1/', include('api.urls')),
    path('api/', include('api.urls')),
]
