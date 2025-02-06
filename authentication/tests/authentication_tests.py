# import pytest
# from django.contrib.auth import get_user_model
# from rest_framework.test import APIClient
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.urls import reverse
# from authentication.models import AddUserInfo

# User = get_user_model()

# @pytest.fixture
# def api_client():
#     """Fixture for creating an API client."""
#     return APIClient()

# @pytest.fixture
# def create_user(db):
#     """Fixture for creating a test user."""
#     user = User.objects.create_user(username="testuser", password="password123")
#     AddUserInfo.objects.create(user=user, bio="Local Bio")
#     return user

# @pytest.fixture
# def get_refresh_token(create_user):
#     """Fixture for generating a refresh token for the test user."""
#     return RefreshToken.for_user(create_user)

# @pytest.fixture
# def authenticated_client(api_client, get_refresh_token):
#     """Fixture for an authenticated API client with JWT token."""
#     api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_refresh_token.access_token}")
#     return api_client

# class TestAuthentication:
#     def test_registration(self, api_client,db):
#         """Test user registration."""
#         url = reverse("register")
#         data = {"username": "testharsh", "email": "harsh@gmail.com", "password": "harsh123", "password2": "harsh123"}
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert User.objects.count() == 1  

#     def test_user_login(self, api_client, create_user):
#         """Test user login."""
#         url = reverse("login")
#         data = {"username": "testuser", "password": "password123"}
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_200_OK

#     def test_user_logout(self, authenticated_client, get_refresh_token):
#         """Test user logout."""
#         url = reverse("logout")
#         data = {"refresh": str(get_refresh_token)}
#         response = authenticated_client.post(url, data)
#         assert response.status_code == status.HTTP_200_OK

#     def test_refresh_token(self, api_client, get_refresh_token):
#         """Test JWT refresh token endpoint."""
#         url = reverse("token_refresh")
#         data = {"refresh": str(get_refresh_token)}
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_200_OK














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
