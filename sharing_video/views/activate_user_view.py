from enum import Enum

from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sharing_video.authentication.authentications import TokenForActivateUser
from sharing_video.exceptions.user_exceptions import ActivateCodeUserNotMatch
from sharing_video.services.user_services import UserServices, InputInformation


class ResponseCode(Enum):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    INVALID_DATA = 'INVALID_DATA'
    ACTIVATE_CODE_NOT_FOUND = 'ACTIVATE_CODE_NOT_FOUND'


class ActivateUserView(APIView):
    authentication_classes = [TokenForActivateUser]

    def __init__(self):
        super().__init__()
        self.service = UserServices()

    def post(self, request):
        input_data = InputInformation(data=request.data)
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
        activate_code = input_data.data['activate_code']
        try:
            self.service.confirm_email(code=activate_code, user=request.user)
            data = {
                'success': True,
                'status_code': ResponseCode.SUCCESS.value,
                'message': ResponseCode.SUCCESS.value,
            }
            return Response(
                status=status.HTTP_200_OK,
                data=data
            )
        except ActivateCodeUserNotMatch:
            data = {
                'success': False,
                'status_code': ResponseCode.ACTIVATE_CODE_NOT_FOUND.value,
                'message': ResponseCode.ACTIVATE_CODE_NOT_FOUND.value
            }
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=data
            )
