from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication


class TokenAuthentication(JWTStatelessUserAuthentication):
    keyword = "Bearer"


class AllowAnyGet(BasePermission):
    """
    Allows access for non-authenticated users for get requests
    """

    def has_permission(self, request, view):
        return request.method == 'GET'
