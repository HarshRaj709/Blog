from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Blog
from .serializers import UserRegistration
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins,generics
from django.contrib.auth.models import User


# Create your views here.
# class Blog_all(ModelViewSet):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer



# Using APIView

# class UserRegistrationView(APIView):
#     def post(self,request,format=None):
#         serializer = UserRegistration(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({'message':'user created successfully'},status=status.HTTP_201_CREATED)
#         else:
#             return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


#Using mixins
# class UserRegistrationView(mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistration

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*kwargs,**kwargs)


#using Generic
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistration
    