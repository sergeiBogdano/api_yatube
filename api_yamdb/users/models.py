from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

ROLES = [
    (ROLE_USER, 'Пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
]


class CustomUserManager(UserManager):
    """Пользовательский менеджер."""

    def create_user(self, username, email, password, **extra_fields):
        """Создание пользователя."""
        if not email:
            raise ValueError('Email is required')
        if username.lower() == 'me':
            raise ValueError('"me" is invalid username')
        return super().create_user(
            username, email=email, password=password, **extra_fields
        )

    def create_superuser(self, username, email, password, **extra_fields):
        """Создание суперпользователя."""
        extra_fields.setdefault('role', ROLE_ADMIN)
        return super().create_superuser(
            username, email, password, **extra_fields
        )


class User(AbstractUser):
    """Модель пользователя."""

    role = models.CharField(
        choices=ROLES,
        default=ROLE_USER,
        blank=False,
        null=False,
        max_length=20,
        verbose_name='Роль',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Юзернейм',
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Username содержит недопустимые символы!'
            )
        ]
    )
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        """Проверка, является ли пользователь администратором."""
        return self.role == ROLE_ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        """Проверка, является ли пользователь модератором."""
        return self.role == ROLE_MODERATOR

    def __str__(self):
        return self.username
