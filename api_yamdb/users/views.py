from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from api_yamdb.settings import FROM_EMAIL
from users.models import User
from users.serializers import (
    AdminSerializer,
    StandartUserSerializer,
    TokenSerializer,
)


class SignUpAPI(APIView):
    """API endpoint для регистрации пользователя."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Обработка регистрации пользователя."""
        serializer = StandartUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        try:
            existing_user = User.objects.get(email=email)

            if existing_user.username != username:
                return Response(
                    {'email': 'Пользователь с таким email уже существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = existing_user

        except User.DoesNotExist:
            if User.objects.filter(username=username).exists():
                return Response(
                    {'username': 'Пользователь с таким username уже существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.create(email=email, username=username)

        confirmation_code = default_token_generator.make_token(user)

        send_mail(
            subject='YaMDb: Код подтверждения',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )


class GetTokenAPI(APIView):
    """Представление для получения токена."""

    permission_classes = (AllowAny,)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Процедура обработки POST-запроса."""
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )

        if not default_token_generator.check_token(
                user, serializer.validated_data['verification_code']):
            return Response(
                {'verification_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )

        access_token = AccessToken.for_user(user)
        return Response(
            {'token': str(access_token)},
            status=status.HTTP_200_OK
        )


class UserDataAPI(APIView):
    """Представление для работы обычного пользователя с его данными."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Процедура обработки GET-запроса."""
        user = request.user
        serializer = StandartUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request: HttpRequest) -> HttpResponse:
        """Процедура обработки PATCH-запроса."""
        user = request.user
        serializer = StandartUserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminDataAPI(ModelViewSet):
    """Представление для администратора для работы с данными пользователей."""

    queryset = User.objects.all()
    serializer_class = AdminSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def update(self, request, *args, **kwargs):
        """Переопределение обновления для обработки PATCH-запросов."""
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
