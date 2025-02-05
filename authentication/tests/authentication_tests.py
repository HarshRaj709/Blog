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
def setup_test_data(db):
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="password123")
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    user_info = AddUserInfo.objects.create(user=user, bio="Local Bio")

    return {
        "client": client,
        "user": user,
        "refresh": refresh,
    }

class TestAuthentication:
    def test_registration(self, setup_test_data):
        url = reverse("register")
        data = {"username": "testharsh","email": "harsh@gmail.com","password": "harsh123","password2": "harsh123"}
        response = setup_test_data["client"].post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() > 1  

    def test_user_login(self, setup_test_data):
        url = reverse("login")
        data = {"username": "testuser", "password": "password123"}
        response = setup_test_data["client"].post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_user_logout(self, setup_test_data):
        url = reverse("logout")
        data = {"refresh": str(setup_test_data["refresh"])}
        response = setup_test_data["client"].post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_refresh_token(self, setup_test_data):
        url = reverse("token_refresh")
        data = {"refresh": str(setup_test_data["refresh"])}
        response = setup_test_data["client"].post(url, data)
        assert response.status_code == status.HTTP_200_OK
