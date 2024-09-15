import json
from enum import Enum

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from notification.enums.type_group_consumer import GroupTypeConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = GroupTypeConsumer.NOTIFICATION.value
        # print(self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': 'ahuhu'
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))

    def notify(self, event):
        message = event['text']
        self.send(text_data=json.dumps({
            'type': GroupTypeConsumer.NOTIFICATION.value,
            'message': message
        }))

