from django.contrib import admin

from titles.models import Category, Genre, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Конфигурация панели администратора для модели Category."""

    list_display = ('pk', 'name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Конфигурация панели администратора для модели Title."""

    list_display = ('pk', 'name', 'year', 'description', 'category')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Конфигурация панели администратора для модели Genre."""

    list_display = ('pk', 'name', 'slug')
