from rest_framework import serializers

from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзыва."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:

        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', 'author', 'title')

    def create(self, validated_data) -> None:
        title_id = self.context['view'].kwargs.get('title_id')
        title = Title.objects.get(id=title_id)

        validated_data.pop('title', None)
        if Review.objects.filter(
            title=title,
            author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError('нельзя оставить отзыв дважды')
        return Review.objects.create(title=title, **validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор комментария."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:

        model = Comment
        fields = '__all__'
        extra_kwargs = {'review': {'read_only': True}}

