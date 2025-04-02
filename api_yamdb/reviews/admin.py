from django.contrib import admin

from reviews.models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Review."""

    list_display = ('pk', 'text', 'score', 'pub_date', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройки админ-панели для модели Comment."""

    list_display = ('pk', 'text', 'author', 'pub_date', 'review')
