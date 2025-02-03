from rest_framework import serializers
from .models import Blog,Category
from authentication.models import AddUserInfo
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken

class AddUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddUserInfo
        fields = ["bio","profile_picture"]
        read_only_fields = ['user']

class BlogSerializer(serializers.ModelSerializer):
    writer = serializers.CharField(source='writer.username', read_only=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)  # Show category name

    class Meta:
        model = Blog
        fields = ['id', 'writer', 'title', 'content', 'category', 'category_name', 'content_image', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

    def validate(self, data):
        category_name = data['category_name']
        if Category.objects.filter(category_name=category_name).exists():
            raise serializers.ValidationError('Category already Exists')
        return data


    




# questions:
    #1. how we store refresh and access token in frontend?