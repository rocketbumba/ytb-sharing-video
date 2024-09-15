from django.core.cache import cache
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from sharing_video.authentication.authentications import CustomTokenAuthentication


class LoginView(ObtainAuthToken):
    authentication_classes = [CustomTokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        cache.set(token, user, 300000)
        return Response({
            'token': token.key,
        })
