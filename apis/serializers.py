from rest_framework import serializers
from .models import Blog
from django.contrib.auth.models import User

# class BlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Blog
#         fields = '__all__'

class UserRegistration(serializers.ModelSerializer):
    password = serializers.CharField(required = True,write_only=True)       #now only username and email will show in the response

    class Meta:
        model = User
        fields = ['username','email','password']            #,'password2'

    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already used by other user.')
        return value

    def validate(self,data):
        username = data.get('username')
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError('username already used, try with different username')
        return data
    
    # def validate(self,data):
    #     if data['password']!=data['password2']:
    #         raise serializers.ValidationError('Password do not match')
    #     return data
    
    def create(self, validated_data):
        # validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
