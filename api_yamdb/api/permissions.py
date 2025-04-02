from rest_framework import permissions

MODERATOR_METHODS = ("PATCH", "DELETE")


class IsAdmin(permissions.BasePermission):
    """Разрешение для администраторов."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение: только админ может изменять, остальные — только читать."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
            or request.user.is_superuser
        )


class IsAuthorOrModerator(permissions.BasePermission):
    """Разрешение: автор или модератор может редактировать."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in MODERATOR_METHODS and request.user.is_moderator
            or obj.author == request.user
        )


class OwnResourcePermission(permissions.BasePermission):
    """Разрешение: только автор, админ или модератор могут изменять."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.method in ["PATCH", "DELETE"]:
            return obj.author == request.user or request.user.is_admin or request.user.is_moderator
        return False


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """Разрешение: автор, админ или модератор могут изменять."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
                or request.method == "POST"
            )
        return request.method in permissions.SAFE_METHODS


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешение: только админ может изменять, остальные — только читать."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )
