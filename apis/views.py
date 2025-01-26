from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Blog
from .serializers import UserRegistration, LoginSerializers,BlogSerializer
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins,generics
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin


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
    
class Listofall(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CreateBlog(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):       #this method runs after the serialization found to be valid
        serializer.save(writer=self.request.user)

class UpdateBlog(UpdateAPIView):
    permission_classes = [IsOwnerOrAdmin,IsAuthenticated]           #Unauthorized users receive a 403 Forbidden or 401 Unauthorized response
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class DeleteBlog(DestroyAPIView):
    permission_classes = [IsOwnerOrAdmin,IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Blog '{instance.title}' has been successfully deleted."},status=status.HTTP_204_NO_CONTENT)
    
# class UserBlog(APIView):
#     permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
#     def get(self,request,format=None):
#         blogs = Blog.objects.filter(writer=request.user)
#         serializer = BlogSerializer(blogs,many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)

class UserBlog(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user)
    





    