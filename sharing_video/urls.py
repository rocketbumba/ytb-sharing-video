from django.urls import path

from sharing_video.views.activate_user_view import ActivateUserView
from sharing_video.views.get_list_video_shared_view import GetListSharingVideoView
from sharing_video.views.login_view import LoginView
from sharing_video.views.logout_view import LogOutView
from sharing_video.views.register_user_view import RegisterUserView
from sharing_video.views.sharing_video_view import SharingVideoView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogOutView.as_view()),
    path('register', RegisterUserView.as_view()),
    path('activate-user', ActivateUserView.as_view()),
    path('create-share-video', SharingVideoView.as_view()),
    path('get_shared-video', GetListSharingVideoView.as_view())
]