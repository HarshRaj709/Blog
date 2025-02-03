# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.urls import reverse
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.contrib.auth import get_user_model
# from .models import AddUserInfo

# class APIEndpointsTests(APITestCase):       #pytest
#     def setUp(self):
#         User = get_user_model() 
#         self.user = User.objects.create_user(username="testuser", password="password123")
#         self.refresh = RefreshToken.for_user(self.user)
#         self.access_token = str(self.refresh.access_token)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
# #image handling
#         with open('/home/savera/Downloads/PHOTO.jpeg', 'rb') as f:
#             image_data = f.read()
#         self.image = SimpleUploadedFile(name='image.jpg', content=image_data, content_type='image/jpeg')
#         AddUserInfo.objects.create(user=self.user, bio="Local Bio",profile_picture=self.image)

# # Create your tests here.
#     def test_registration(self):
#         url = reverse("register")
#         data = {"username":"testharsh","email":"harsh@gmail.com","password":"harsh123","password2":"harsh123"}
#         self.assertEqual(status.HTTP_201_CREATED, self.client.post(url, data).status_code)
#         self.assertGreater(User.objects.count(), 1)

#     def test_userlogin(self):
#         url = reverse("login")
#         data = {"username":"testuser","password":"password123"}
#         response = self.client.post(url, data)
#         self.assertEqual(status.HTTP_200_OK,response.status_code)
#         # print(response.data)

#     def test_userlogout(self):
#         url = reverse("logout")
#         data = {"refresh":self.refresh}
#         response = self.client.post(url,data)
#         self.assertEqual(status.HTTP_200_OK,response.status_code)

#     #Refresh token testing

#     def test_refreshtoken(self):
#         url = reverse("token_refresh")
#         data = {"refresh":self.refresh}
#         response = self.client.post(url,data)
#         self.assertEqual(status.HTTP_200_OK,response.status_code)