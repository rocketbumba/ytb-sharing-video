import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, UserManager
from django.core.cache import cache
from django.db import transaction
from django.apps import apps
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from sharing_video.exceptions.common_exceptions import UnknowException
from sharing_video.exceptions.user_exceptions import UsernameExists, ActivateCodeUserNotMatch


class InputInformation(serializers.Serializer):
    activate_code = serializers.IntegerField(required=True)


class InputUserInformation(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=256)
    password = serializers.CharField(required=True, max_length=256)
    email = serializers.EmailField(required=True, max_length=256)


class UserServices(UserManager):

    def __init__(self):
        pass

    def register_user(self, user_information: InputUserInformation):
        return self.__register_user(user_information)

    def confirm_email(self, code: str, user: User):
        self.__confirm_email(code, user)

    def __is_existing_username(self, username: str) -> bool:
        return User.objects.filter(username=username).exists()

    @transaction.atomic
    def __register_user(self, user_information):
        if self.__is_existing_username(user_information['username']):
            raise UsernameExists()
        try:

            user = User.objects.create_user(
                username=user_information['username'],
                password=user_information['password'],
                email=user_information['email'],
            )
            random_number = random.randint(1000, 9999)
            # user.email_user('Confirm Email', 'You have successfully registered. Please use this code to activate your '
            #                                  'account.' + str(random_number) + '. It will expired after 5 minutes')
            cache.set(user.pk, random_number, 3000000)
            token, created = Token.objects.get_or_create(user=user)
            cache.set(token, user, 3000000)
            cache.get(user.pk)
            return user, token

        except Exception as e:
            raise UnknowException(e.__str__())

    @staticmethod
    def __confirm_email(code: str, user: User):
        print(user.pk)
        save_code = cache.get(user.pk)
        print(save_code)
        if code != save_code:
            raise ActivateCodeUserNotMatch()
        else:
            user.is_active = True
            user.save()

    def logout_user(self, user: User):
        self.__logout_user(user)

    @staticmethod
    def __logout_user(user: User):
        try:
            print(user)
            token = Token.objects.get(user=user)
            cache.delete(token)
            token.delete()
        except Exception as e:
            raise UnknowException(e.__str__())
