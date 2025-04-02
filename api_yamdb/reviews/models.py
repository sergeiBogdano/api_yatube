from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from titles.models import Title
from users.models import User


class Review(models.Model):
    """Модель отзыва."""

    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        'оценка',
        validators=[
            MinValueValidator(1, 'минимальная оценка 1'),
            MaxValueValidator(10, 'максимальная оценка 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название',
    )

    class Meta:

        constraints = [
            UniqueConstraint(
                fields=['author', 'title'],
                name='constraints_review'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    """Модель комментария."""

    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text
