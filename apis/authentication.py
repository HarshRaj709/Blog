from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

class CookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None
        
        try:
            validated_token = AccessToken(token)
            user_id = validated_token['user_id']
            user = User.objects.get(id=user_id)
            return (user, None)  # Return authenticated user and no auth information
        except Exception as e:
            raise AuthenticationFailed("Invalid token: " + str(e))