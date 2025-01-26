from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Blog
from .serializers import UserRegistration, LoginSerializers
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins,generics
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework.permissions import IsAuthenticated


# Create your views here.
# class Blog_all(ModelViewSet):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer






#Using mixins
# class UserRegistrationView(mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistration

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*kwargs,**kwargs)


def get_tokens(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }


# Using APIView

class UserRegistrationView(APIView):
    def post(self,request,format=None):
        serializer = UserRegistration(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens(user)
            response = Response({"msg":'User created successfull',"token":token['access']},status=status.HTTP_200_OK)
            response.set_cookie(key='access_token',value=token,httponly=True,secure=False,samesite='Lax')
            # return Response({"token":token})
            return response
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#using Generic
# class UserRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistration


class LoginUser(APIView):
    def post(self,request,format=None):
        serializer = LoginSerializers(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                token = get_tokens(user)
                #print(token['access'])
                response = Response({"msg":'Login Successful'},status=status.HTTP_200_OK)
                response.set_cookie(key='access_token',value=token['access'],httponly=True,secure=False,samesite='Lax')
                return response
                # return Response({"token":token,'msg':'Login Successful'},status=status.HTTP_200_OK)
            else:
                response = Response({"msg":'credentials not matched'},status=status.HTTP_400_BAD_REQUEST)
                response.delete_cookie('access_token')
                return response
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        username = request.user.username
        logout(request)
        response = Response({"message":"Logged out","username":username},status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        return response




    