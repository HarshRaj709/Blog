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
    


class LoginUser(CreateAPIView):
    serializer_class = LoginSerializers
    MAX_FAILED_ATTEMPTS = 3  # Maximum allowed failed login attempts

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(username=username)
            user_info = AddUserInfo.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"msg": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # Attempt authentication
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            # Reset failed login attempts on successful login
            user_info.failed_login_attempts = 0
            user_info.save()

            # Generate tokens for the user
            token = get_tokens(authenticated_user)
            return Response({"msg": "Login Successful", "token": token}, status=status.HTTP_200_OK)
        return Response({"Error":'Wrong Credentials'},status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         # Increment failed login attempts
    #         user_info.failed_login_attempts += 1
    #         user_info.save()

    #         # Check if the maximum failed attempts have been reached
    #         if user_info.failed_login_attempts >= self.MAX_FAILED_ATTEMPTS:
    #             # Blacklist all tokens for the user
    #             self.blacklist_user_tokens(user)  # Pass the User object
    #             return Response(
    #                 {"msg": "Too many failed attempts. All sessions have been logged out."},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
    #         else:
    #             return Response({"msg": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    # def blacklist_user_tokens(self, user):
    #     try:
    #         # Retrieve all outstanding tokens for the user
    #         outstanding_tokens = OutstandingToken.objects.filter(user=user)

    #         for token in outstanding_tokens:
    #             # Check if the token is already blacklisted
    #             if not BlacklistedToken.objects.filter(token=token).exists():
    #                 # Blacklist the token
    #                 BlacklistedToken.objects.create(token=token)

    #         print(f"All tokens blacklisted for user: {user.username}")
    #     except Exception as e:
    #         print(f"Error blacklisting tokens for user {user.username}: {e}")


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