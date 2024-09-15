from enum import Enum

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from sharing_video.exceptions.common_exceptions import UnknowException
from sharing_video.exceptions.user_exceptions import UsernameExists
from sharing_video.services.user_services import InputUserInformation, UserServices


class ResponseCode(Enum):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    INVALID_DATA = 'INVALID_DATA'
    USER_EXISTS = 'USER_EXISTS'


class RegisterUserView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserServices()

    def post(self, request):
        input_data = InputUserInformation(data=request.data)
        if not input_data.is_valid():
            data = {
                'success': False,
                'status_code': ResponseCode.INVALID_DATA.value,
                'message': ResponseCode.INVALID_DATA.value
            }
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=data
            )

        try:
            user, token = self.service.register_user(user_information=input_data.data)
            data = {
                'success': True,
                'status_code': ResponseCode.SUCCESS.value,
                'message': ResponseCode.SUCCESS.value,
                'token': token.key
            }
            return Response(
                status=status.HTTP_200_OK,
                data=data
            )
        except UnknowException as error:
            data = {
                'success': False,
                'status_code': ResponseCode.UNKNOWN_ERROR.value,
                'message': str(error)
            }
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=data
            )
        except UsernameExists as error:
            data = {
                'success': False,
                'status_code': ResponseCode.USER_EXISTS.value,
                'message': ResponseCode.USER_EXISTS.value
            }
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=data
            )
