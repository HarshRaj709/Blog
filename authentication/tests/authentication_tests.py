import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.models import AddUserInfo  # Adjust import if needed

User = get_user_model()

@pytest.mark.django_db      #if not used that try to perform database operations then will get error
class TestAPIEndpoints:
    @pytest.fixture(autouse=True)       #this will allow to apply fixture on each testcase we include teardown code in fixture which runs after eecution of function.
    def setup(self, db):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")
        
        with open('/home/savera/Downloads/PHOTO.jpeg', 'rb') as f:
            image_data = f.read()
        self.image = SimpleUploadedFile(name='image.jpg', content=image_data, content_type='image/jpeg')
        self.user_info = AddUserInfo.objects.create(user=self.user, bio="Local Bio", profile_picture=self.image)
    
    def test_registration(self):
        url = reverse("register")
        data = {"username": "testharsh", "email": "harsh@gmail.com", "password": "harsh123", "password2": "harsh123"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() > 1

    def test_userlogin(self):
        url = reverse("login")
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_userlogout(self):
        url = reverse("logout")
        data = {"refresh": str(self.refresh)}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_refreshtoken(self):
        url = reverse("token_refresh")
        data = {"refresh": str(self.refresh)}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

#if failed

# assert response.status_code == status.HTTP_201_CREATED
# E       assert 200 == 201
# E        +  where 200 = <Response status_code=200, "application/json">.status_code
# E        +  and   201 = status.HTTP_201_CREATED
