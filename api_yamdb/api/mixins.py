from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins, viewsets


class BaseViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет с поддержкой пагинации."""

    pagination_class = LimitOffsetPagination


class ListCreateViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для создания, просмотра и удаления объектов."""

    pagination_class = LimitOffsetPagination


class ListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для просмотра списка и отдельного объекта."""

    pagination_class = LimitOffsetPagination
