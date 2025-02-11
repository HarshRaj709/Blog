from .models import Blog,Category
from authentication.models import AddUserInfo
from .serializers import BlogSerializer,CategorySerializer,AddUserInfoSerializer
from rest_framework.generics import ListAPIView,UpdateAPIView,CreateAPIView,DestroyAPIView,GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin
from rest_framework.filters import SearchFilter


#Blogs APi
class Listofall(ListAPIView):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title','category__category_name','writer']               

class CreateBlog(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer

    def perform_create(self, serializer):       
        serializer.save(writer=self.request.user)

class UpdateBlog(UpdateAPIView):
    permission_classes = [IsOwnerOrAdmin,IsAuthenticated]           
    queryset = Blog.objects.all().order_by('-updated_at')
    serializer_class = BlogSerializer


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

class DeleteBlog(DestroyAPIView):
    permission_classes = [IsOwnerOrAdmin,IsAuthenticated]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Blog '{instance.title}' has been successfully deleted."},status=status.HTTP_204_NO_CONTENT)
    

class UserBlog(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
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
                return Response({"msg":f"{user_info.user.username} Info added successfully"},status=status.HTTP_201_CREATED)
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
            user_email = request.user.email
            user_info = AddUserInfo.objects.get(user=request.user)
            user_serializer = AddUserInfoSerializer(user_info)
            
            blogs_info = Blog.objects.filter(writer=request.user)
            blogs_serializer = BlogSerializer(blogs_info,many=True)
            
            return Response({"username":request.user.username,"user_email":user_email,"user info":user_serializer.data,"blogs":blogs_serializer.data},status=status.HTTP_200_OK)
        except AddUserInfo.DoesNotExist:
            return Response({"msg":"User Info not found"},status=status.HTTP_404_NOT_FOUND)