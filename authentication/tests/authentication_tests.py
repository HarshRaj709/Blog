import pytest
from django.contrib.auth import get_user_model  #useful if you create a custom user model then it will fetch custom user model.
from rest_framework.test import APIClient
from rest_framework import status
# from django.contrib.auth.models import User       #fetches the defalut user model
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from authentication.models import AddUserInfo  # Adjust import if needed

User = get_user_model()

@pytest.mark.django_db      #if not used and try to perform database operations then will get error
class TestAPIEndpoints:     #class name must start with Test
    @pytest.fixture()       #autouse = True       #this will allow to apply fixture on each testcase we include teardown code in fixture which runs after execution of function.---use yield for that
    def setup(self, db):        #We can give any name to fixtures
        """THis is Docstring for Authentication testing Fixtures"""
        self.client = APIClient()       #Simulates API requests (GET, POST, PUT, etc.)
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")
        
        with open('/home/savera/Downloads/PHOTO.jpeg', 'rb') as f:
            image_data = f.read()
        self.image = SimpleUploadedFile(name='image.jpg', content=image_data, content_type='image/jpeg')
        self.user_info = AddUserInfo.objects.create(user=self.user, bio="Local Bio", profile_picture=self.image)
        # yield
        # print('Teardown')


    def test_registration(self,setup):
        url = reverse("register")
        data = {"username": "testharsh", "email": "harsh@gmail.com", "password": "harsh123", "password2": "harsh123"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() > 1
        # print(User.objects.count())     #2
        

    def test_userlogin(self,setup):
        url = reverse("login")
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_userlogout(self,setup):
        url = reverse("logout")
        data = {"refresh": str(self.refresh)}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_refreshtoken(self,setup):
        url = reverse("token_refresh")
        data = {"refresh": str(self.refresh)}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

# #if failed

# # assert response.status_code == status.HTTP_201_CREATED
# # E       assert 200 == 201
# # E        +  where 200 = <Response status_code=200, "application/json">.status_code
# # E        +  and   201 = status.HTTP_201_CREATE


# import pytest

# Using parametrize to test with different values
@pytest.mark.parametrize("x, y, expected_sum", [(1, 2, 3), (4, 5, 9), (7, 8, 15)])  #counted as 3
def test_addition(x, y, expected_sum):  # ✅ Correct indentation
        result = x + y
        assert result == expected_sum


# def multiply(x,y):
#     return x*y

# @pytest.mark.parametrize("a,b,expected_result",[(2,3,6),(4,2,8),(3,1,3)])
# def test_multiply(a,b,expected_result):
#     assert multiply(a,b) == expected_result

# def divide(a,b):
#     if b == 0:
#         raise ValueError("Can not divide by zero")
#     return a/b

# @pytest.mark.parametrize("a,b,expected_result",[(10,5,2),(20,5,4),(10,0,ValueError)])
# def test_divide(a,b,expected_result):
#     if expected_result == ValueError:
#         with pytest.raises(ValueError):
#             divide(a,b)
#     else:
#         assert divide(a,b) == expected_result

