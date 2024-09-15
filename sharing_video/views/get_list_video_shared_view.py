from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sharing_video.exceptions.common_exceptions import UnknowException
from sharing_video.services.share_video_services import ShareVideoService, OutputCreateShareVideo


class GetListSharingVideoView(APIView):
    def __init__(self):
        super().__init__()
        self.service = ShareVideoService()

    def get(self, request):
        try:
            output_data = self.service.get_share_videos()
            response_data = OutputCreateShareVideo(output_data, many=True)
            return Response(data=response_data.data, status=status.HTTP_200_OK)
        except UnknowException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
