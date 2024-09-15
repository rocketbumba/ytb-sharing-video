from enum import Enum

from django.core.cache import cache
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from sharing_video.authentication.authentications import CustomTokenAuthentication
from sharing_video.services.user_services import UserServices


class ResponseCode(Enum):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    INVALID_DATA = 'INVALID_DATA'
    USER_EXISTS = 'USER_EXISTS'


class LogOutView(APIView):
    authentication_classes = [CustomTokenAuthentication]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserServices()

    def post(self, request, *args, **kwargs):
        print(request.user)
        try:
            self.service.logout_user(request.user)
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            data = {
                'success': False,
                'status_code': ResponseCode.UNKNOWN_ERROR.value,
                'message': str(error)
            }
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=data
            )
