from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication


class TokenAuthentication(JWTStatelessUserAuthentication):
    keyword = "Bearer"


class IsAuthenticatedGetIsAdminPost(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return bool(request.user and request.user.is_authenticated)
        else:
            return bool(request.user and request.user.is_staff)

