from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import CommentsViewSet, ReviewViewSet
from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet
from users.views import AdminDataAPI, GetTokenAPI, SignUpAPI, UserDataAPI

router_v1 = DefaultRouter()
router_v1.register("users", AdminDataAPI, basename="users")
router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="reviews",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentsViewSet,
    basename="comments",
)

urlpatterns = [
    path("v1/users/me/", UserDataAPI.as_view(), name="me"),
    path("v1/auth/signup/", SignUpAPI.as_view(), name="signup"),
    path("v1/auth/token/", GetTokenAPI.as_view(), name="token"),
    path("v1/", include(router_v1.urls)),
]
