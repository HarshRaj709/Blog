from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Blog,Category,AddUserInfo
from .serializers import UserRegistration, LoginSerializers,BlogSerializer,CategorySerializer,AddUserInfoSerializer
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView,GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins,generics
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
from rest_framework.filters import SearchFilter,OrderingFilter


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

# class UserRegistrationView(APIView):
#     def post(self,request,format=None):
#         serializer = UserRegistration(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token = get_tokens(user)
#             response = Response({"msg":'User created successfull',"token":token['access']},status=status.HTTP_200_OK)
#             response.set_cookie(key='access_token',value=token['access'],httponly=True,secure=False,samesite='Lax')
#             # return Response({"token":token})
#             return response
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#using Generic
class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistration
    def post(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token = get_tokens(user)
                return Response({"msg": "User created successfull", "token": token}, status=status.HTTP_201_CREATED)
            return Response({"msg": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(CreateAPIView):
    serializer_class = LoginSerializers
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'],password=serializer.validated_data['password'])
        if user is not None:
            token = get_tokens(user)
            return Response({"msg": "Login Successful", "token": token}, status=status.HTTP_200_OK)
        return Response({"msg": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# class LoginUser(APIView):
#     def post(self,request,format=None):
#         # response = Response(status=status.HTTP_200_OK)
#         # response.delete_cookie('access_token')
#         serializer = LoginSerializers(data = request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data.get('username')
#             password = serializer.validated_data.get('password')
#             user = authenticate(username=username,password=password)
#             if user is not None:
#                 token = get_tokens(user)
#                 #print(token['access'])
#                 response = Response({"msg":'Login Successful'},status=status.HTTP_200_OK)
#                 # response.set_cookie(key='access_token',value=token['access'],httponly=True,secure=False,samesite='Lax')
#                 return response
#                 # return Response({"token":token,'msg':'Login Successful'},status=status.HTTP_200_OK)
#             else:
#                 response = Response({"msg":'credentials not matched'},status=status.HTTP_400_BAD_REQUEST)
#                 response.delete_cookie('access_token')
#                 return response
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# class LogoutUser(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self,request,format=None):
#         username = request.user.username
#         logout(request)
#         response = Response({"message":"Logged out","username":username},status=status.HTTP_200_OK)
#         response.delete_cookie('access_token')
#         return response

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
    
class CategoryView(APIView):
    def get(self,request,format=None):
        Categories = Category.objects.all()
        serializer = CategorySerializer(Categories,many=True)
        if serializer:
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def post(self,request,format=None):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            category_name = serializer.validated_data['category_name']
            return Response({"message":f"category added successfully {category_name}"},status=status.HTTP_201_CREATED)


#Blogs APi


class Listofall(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title','category__category_name','writer']               #?search=mera

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
    

class UserInfoViews(CreateAPIView):
    serializer_class = AddUserInfoSerializer
    permission_classes = [IsOwnerOrAdmin,IsAuthenticated]
    def post(self,request,format=None):
        try:
            user_info = AddUserInfo.objects.get(user=request.user)
            serializer = self.get_serializer(user_info, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"msg":"User Info added successfully"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except AddUserInfo.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"msg":"User Info added successfully"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class GetUserInfo(ListAPIView):
    permission_classes = [IsAuthenticated,IsOwnerOrAdmin]
    serializer_class = AddUserInfoSerializer
    
    def get(self,request,*args,**kwargs):
        try:
            user_info = AddUserInfo.objects.get(user=request.user)
            user_serializer = AddUserInfoSerializer(user_info)
            
            blogs_info = Blog.objects.filter(writer=request.user)
            blogs_serializer = BlogSerializer(blogs_info,many=True)
            
            return Response({"username":request.user.username,"user info":user_serializer.data,"blogs":blogs_serializer.data},status=status.HTTP_200_OK)
        except AddUserInfo.DoesNotExist:
            return Response({"msg":"User Info not found"},status=status.HTTP_404_NOT_FOUND)
        

        
    





    