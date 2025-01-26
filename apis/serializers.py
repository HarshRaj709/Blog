from rest_framework import serializers
from .models import Blog,Category
from django.contrib.auth.models import User

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

class UserRegistration(serializers.ModelSerializer):
    password2 = serializers.CharField(required = True,write_only=True)       #now only username and email will show in the response

    class Meta:
        model = User
        fields = ['username','email','password','password2']            #

    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already used by other user.')
        return value

    def validate(self,data):
        username = data.get('username')
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError('username already used, try with different username')
        return data
    
    def validate(self,data):
        if data['password']!=data['password2']:
            raise serializers.ValidationError('Password do not match')
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(required=True)
