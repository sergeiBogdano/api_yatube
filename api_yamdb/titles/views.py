from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.serializers import ModelSerializer

from api.mixins import BaseViewSet, ListCreateViewSet
from api.permissions import AdminOrReadOnly
from titles.filters import TitleFilter
from titles.models import Category, Genre, Title
from titles.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
)


class CategoryViewSet(ListCreateViewSet):
    """Viewset для категорий."""

    permission_classes = (AdminOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateViewSet):
    """Viewset для жанров."""

    permission_classes = (AdminOrReadOnly,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(BaseViewSet):
    """Viewset для произведений."""

    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    permission_classes = (AdminOrReadOnly,)
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self) -> ModelSerializer:
        """Указать сериализатор для чтения или записи."""
        if self.action in ['list', 'retrieve']:
            return TitleSerializerRead
        return TitleSerializerWrite
