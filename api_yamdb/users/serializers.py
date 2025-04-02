from django.core.validators import RegexValidator
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class TokenSerializer(serializers.Serializer):
    """Сериализатор токена."""

    username = serializers.CharField(max_length=150, required=True)
    verification_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        """Проверка юзернейма для токена."""
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(f'Пользователь {value} не найден')
        return value


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя с параметром роли администратора."""

    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username содержит недопустимые символы!'
            ),
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        """Проверка корректности юзернейма."""
        if value.lower() == 'me':
            raise serializers.ValidationError('"me" является недопустимым юзернеймом')
        return value


class StandartUserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username содержит недопустимые символы!'
            )
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        """Проверка юзернейма (без учета регистра для 'me')."""
        if value.lower() == 'me':
            raise serializers.ValidationError('"me" является недопустимым юзернеймом')
        return value
