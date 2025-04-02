from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ModelSerializer

from api.permissions import IsAuthorOrAdminOrModerator
from reviews.models import Review
from reviews.serializers import CommentsSerializer, ReviewSerializer
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для отзывов."""

    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options'
    ]
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Создание отзыва."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self) -> QuerySet:
        """Получить отзывы для viewset."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()


class CommentsViewSet(viewsets.ModelViewSet):
    """Viewset для комментариев."""

    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options'
    ]
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorOrAdminOrModerator]
    pagination_class = LimitOffsetPagination

    def get_review(self) -> Review:
        """Получить объект отзыва на основе параметров URL."""
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(
            Review,
            pk=review_id,
            title__id=title_id,
        )

    def perform_create(self, serializer: ModelSerializer) -> None:
        """Создание комментария."""
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self) -> QuerySet:
        """Получить комментарии для viewset."""
        review = self.get_review()
        return review.comments.all()
