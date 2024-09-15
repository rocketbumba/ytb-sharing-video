from django.core.cache import cache
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user = cache.get(key)
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        return user, key


class TokenForActivateUser(TokenAuthentication):
    def authenticate_credentials(self, key):
        user = cache.get(key)
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid token.')
        return user, key

