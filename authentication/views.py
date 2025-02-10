from .serializers import UserRegistration, LoginSerializers,Password_ResetSerializer,Password_changedSerializer
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import AddUserInfo
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

# Create your views here.


def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistration
    def post(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token = get_tokens(user)
                return Response({"msg": "User created successfull", "token": token}, status=status.HTTP_201_CREATED)
            return Response({"msg":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import AddUserInfo
from .views import get_tokens

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')

        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_OAUTH2_CLIENT_ID)

            # Get user info
            userid = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user
                user = User.objects.create_user(username=email, email=email, first_name=name)
                AddUserInfo.objects.create(user=user)

            # Generate tokens
            tokens = get_tokens(user)

            return Response({
                'msg': 'Login Successful',
                'tokens': tokens,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.first_name,
                }
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)





class LoginUser(CreateAPIView):
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg": "Login Successful", "token": get_tokens(user)}, status=status.HTTP_200_OK)
    

class Password_Reset(APIView):
    def post(self, request, format=None):
        user = request.user
        serializer = Password_ResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Create password reset link
            reset_link = f"{settings.FRONTEND_URL}/auths/reset/{uidb64}/{token}/"

            # Send email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link below to reset your password:\n{reset_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({'msg': 'Email sent to recover the password'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordAPIView(APIView):
    def post(self, request, uidb64, token):  
        refresh = request.data.get('refresh')
        serializer = Password_changedSerializer(data=request.data,context={'uidb64': uidb64, 'token': token,'refresh':refresh}) 
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Password changed Successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #need to blacklist the refresh token


#Generic Logout
class LogoutUser(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        refresh = request.data.get('refresh')
        # print(refresh)
        if not refresh:
            return Response({"msg":"refresh token is required"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                token = RefreshToken(refresh)
                token.blacklist()
                return Response({"msg":"Logged out successfully"},status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"msg":f"Error: {e}"},status=status.HTTP_400_BAD_REQUEST)