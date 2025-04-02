from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from titles.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:

        model = Category
        fields = ['name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:

        model = Genre
        fields = ['name', 'slug']


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор произведения для чтения."""

    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:

        model = Title
        fields = '__all__'


class TitleSerializerWrite(serializers.ModelSerializer):
    """Сериализатор произведения для записи."""

    category = SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:

        model = Title
        fields = '__all__'
