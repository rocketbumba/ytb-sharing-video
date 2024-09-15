import json
from datetime import datetime
from typing import List

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from rest_framework import serializers

from sharing_video.exceptions.common_exceptions import UnknowException
from sharing_video.models import SharingVideo


class InputCreateShareVideo(serializers.Serializer):
    video_url = serializers.CharField(required=True)


class OutputCreateShareVideo(serializers.ModelSerializer):
    class Meta:
        model = SharingVideo
        fields = '__all__'


class ShareVideoService:
    def __init__(self):
        pass
    def create_share_video(self, video_url: str, user: User):
        self.__create_share_video(video_url, user)

    def get_share_videos(self) -> List[SharingVideo]:
        return self.__get_share_videos()

    @staticmethod
    def __get_share_videos():
        video_qs = SharingVideo.objects.filter().order_by('created_at')

        return video_qs

    def __create_share_video(self, video_url: str, user: User):
        try:
            SharingVideo.objects.create(video_url=video_url, user=user)
            channel_layer = get_channel_layer()
            data = "User" + str(user.username) + " has share video "
            async_to_sync(channel_layer.group_send)(
                'test',  # Group Name, Should always be string
                {
                    "type": "notify",
                    "text": data,
                },
            )
        except Exception as e:
            print(e)
            raise UnknowException()
