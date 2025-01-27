import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Blog, Category, AddUserInfo
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class APIEndpointsTests(APITestCase):
    def setUp(self):
        # Set up users, blogs, and categories for testing
        self.user = User.objects.create_user(username="testuser", password="password123")
        #self.admin_user = User.objects.create_superuser(username="admin", password="admin123")
        self.category = Category.objects.create(category_name="Test Category")
        self.blog = Blog.objects.create(title="Test Blog", content="Test content", category=self.category, writer=self.user)
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.image = SimpleUploadedFile("test_image.jpg", content=b'content', content_type="image/jpeg")

    

    def test_registration(self):
        url = reverse("register")
        data = {"username":"testharsh","email":"harsh@gmail.com","password":"harsh123","password2":"harsh123"}
        self.assertEqual(status.HTTP_201_CREATED, self.client.post(url, data).status_code)
        self.assertGreater(User.objects.count(), 1)

    def test_Userlogin(self):
        url = reverse("login")
        data = {"username":"testuser","password":"password123"}
        response = self.client.post(url, data)
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        # print(response.data)

    def test_Userlogout(self):
        url = reverse("logout")
        data = {"refresh":self.refresh}
        response = self.client.post(url,data)
        self.assertEqual(status.HTTP_200_OK,response.status_code)

#Now blogs testing

    def test_list_blogs(self):
        url = reverse('Blogs_get')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_createblogs(self):
        url = reverse('create')
        data = {"title":"Mera Bdla","content":"Mera Bdla content","category":self.category.id}
        response = self.client.post(url,data)
        self.assertEqual(status.HTTP_201_CREATED,response.status_code)

    def test_updateblogs(self):
        url = reverse('update',args=[self.blog.id])
        data = {"title":"Updated title","content":"Updated content","category":self.category.id}
        response = self.client.put(url,data)
        self.assertEqual(status.HTTP_200_OK,response.status_code)

    def test_deleteblog(self):
        url = reverse('delete',args =[self.blog.id])
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT,response.status_code)

    def test_Userblog(self):
        url = reverse('Userblog')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK,response.status_code)
        self.assertGreater(len(response.data),0)

#Refresh token testing

    def test_refreshtoken(self):
        url = reverse("token_refresh")
        data = {"refresh":self.refresh}
        response = self.client.post(url,data)
        self.assertEqual(status.HTTP_200_OK,response.status_code)

#Add user info testing

    # def test_userInfo(self):
    #     url = reverse("adduserinfo")
    #     data = {
    #         "bio": "mera naam sardar h",
    #         "profile_picture": self.image
    #     }
    #     response = self.client.post(url, data, format="multipart")  # Ensure 'multipart' format for file upload
    #     self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    #     # Validate the response contains expected data
    #     self.assertIn("msg", response.data)
    #     self.assertEqual(response.data["msg"], "User Info added successfully")

    def test_getuser(self):
        AddUserInfo.objects.create(user=self.user, bio="This is a test bio")
        url = reverse('userinfo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user info", response.data)