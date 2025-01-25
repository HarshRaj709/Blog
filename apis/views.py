from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Blog
from .serializers import BlogSerializer

# Create your views here.
class Blog_all(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer