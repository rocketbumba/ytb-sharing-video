from enum import Enum

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ytb_sharing_video.authentication.authentications import CustomTokenAuthentication
from sharing_video.exceptions.common_exceptions import UnknowException
from sharing_video.services.share_video_services import ShareVideoService, OutputCreateShareVideo, InputCreateShareVideo


class ResponseCode(Enum):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    INVALID_DATA = 'INVALID_DATA'
    USER_EXISTS = 'USER_EXISTS'


class SharingVideoView(APIView):
    authentication_classes = [CustomTokenAuthentication]

    def __init__(self):
        super().__init__()
        self.service = ShareVideoService()

    def get(self, request):
        try:
            output_data = self.service.get_share_videos()
            response_data = OutputCreateShareVideo(output_data, many=True)
            data = {
                'success': True,
                'status_code': ResponseCode.SUCCESS.value,
                'message': ResponseCode.SUCCESS.value,
                'data': response_data.data
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except UnknowException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        input_data = InputCreateShareVideo(data=request.data)
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
        video_url = input_data.data['video_url']

        try:
            self.service.create_share_video(video_url=video_url, user=request.user)
            data = {
                'success': True,
                'status_code': ResponseCode.SUCCESS.value,
                'message': ResponseCode.SUCCESS.value,
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
