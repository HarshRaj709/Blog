from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from .models import AddUserInfo

class AddUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddUserInfo
        fields = ["bio","profile_picture"]
        read_only_fields = ['user']

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
    password = serializers.CharField(write_only=True,required=True)


class Password_ResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self,value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is wrong')
        return value



class Password_changedSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    password2 = serializers.CharField(write_only=True, required=True, min_length=6)

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        uidb64 = self.context.get('uidb64')
        token = self.context.get('token')

        
        if password != password2:
            raise serializers.ValidationError({'password2': 'Passwords do not match'})

        
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({'uidb64': 'Invalid user ID'})

        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({'token': 'Invalid or expired token'})
        self.user = user
        return data


    def update(self, validated_data):
        user = self.user
        user.set_password(validated_data['password'])
        user.save()
        refresh_token = self.context.get('refresh')  
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                raise serializers.ValidationError({'refresh': 'Failed to blacklist refresh token'})
        return user



