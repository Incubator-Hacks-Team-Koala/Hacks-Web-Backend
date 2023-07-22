from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication


class TokenAuthentication(JWTStatelessUserAuthentication):
    keyword = "Bearer"
