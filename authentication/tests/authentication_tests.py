import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.models import AddUserInfo  

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def user_creation(db):
    user = User.objects.create_user(username="testuser", password="password123")
    AddUserInfo.objects.create(user=user, bio="Local Bio")
    return user

@pytest.fixture
def refresh_token(user_creation):
    refresh =  RefreshToken.for_user(user_creation)
    return refresh

@pytest.fixture
def authenticate_client(client,refresh_token):
    client.credentials(HTTP_AUTHORIZATION = f"Bearer {refresh_token.access_token}")
    return client



class TestAuthentication:
    def test_registration(self, client,db):
        url = reverse("register")
        data = {"username": "testharsh","email": "harsh@gmail.com","password": "harsh123","password2": "harsh123"}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1  

    def test_user_login(self, client,user_creation):
        url = reverse("login")
        data = {"username": "testuser", "password": "password123"}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_user_logout(self, authenticate_client,refresh_token):
        url = reverse("logout")
        data = {"refresh": str(refresh_token)}
        response = authenticate_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_refresh_token(self, client, refresh_token):
        url = reverse("token_refresh")
        data = {"refresh": str(refresh_token)}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
