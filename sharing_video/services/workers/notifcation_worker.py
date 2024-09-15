from ytb_sharing_app.enum.enum_workers import NotificationType
from ytb_sharing_app.models import Task


class NotificationWorker:
    def __init__(self):
        pass

    def __send_noti_to_user(self, user_id: str, video_url: str, user_create: str):
        pass

    def __send_notification(self):
        tasks = Task.objects.filter(type=NotificationType.SEND_TO_ANOTHER_USER)
        current_user_activate = []
        for user in current_user_activate:
            for task in tasks:
                self.__send_noti_to_user(user_id=user, video_url=task.video_url, user_create=task.user)


