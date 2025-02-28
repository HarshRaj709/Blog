# import json
# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken
# from authentication.models import AddUserInfo
# from django.urls import reverse
# from .models import Blog, Category
# from django.core.files.uploadedfile import SimpleUploadedFile

# class APIEndpointsTests(APITestCase):       #pytest
#     def setUp(self):
#         self.user = User.objects.create_user(username="testuser", password="password123")
        
#         self.category = Category.objects.create(category_name="Test Category")
#         self.blog = Blog.objects.create(title="Test Blog", content="Test content", category=self.category, writer=self.user)
#         self.refresh = RefreshToken.for_user(self.user)
#         self.access_token = str(self.refresh.access_token)
#         self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
# #image handling
#         with open('/home/savera/Downloads/PHOTO.jpeg', 'rb') as f:
#             image_data = f.read()
#         self.image = SimpleUploadedFile(name='image.jpg', content=image_data, content_type='image/jpeg')


#     def test_list_blogs(self):
#         url = reverse('Blogs_get')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreater(len(response.data), 0)

#     def test_createblogs(self):
#         url = reverse('create')
#         data = {"title":"Mera Bdla","content":"Mera Bdla content","category":self.category.id,"content_image":self.image}
#         response = self.client.post(url,data)
#         self.assertEqual(status.HTTP_201_CREATED,response.status_code)

#     def test_updateblogs(self):
#         url = reverse('update',args=[self.blog.id])
#         data = {"title":"Updated title","content":"Updated content","category":self.category.id,"content_image":self.image}
#         response = self.client.put(url,data)
#         self.assertEqual(status.HTTP_200_OK,response.status_code)

#     def test_deleteblog(self):
#         url = reverse('delete',args =[self.blog.id])
#         response = self.client.delete(url)
#         self.assertEqual(status.HTTP_204_NO_CONTENT,response.status_code)

#     def test_Userblog(self):
#         url = reverse('Userblog')
#         response = self.client.get(url)
#         #print(response.data)
#         self.assertEqual(status.HTTP_200_OK,response.status_code)
#         self.assertGreater(len(response.data),0)

#     #Add user info testing

#     def test_userInfo(self):
#         url = reverse("adduserinfo")
#         data = {
#             "bio": "mera naam sardar h",
#             "profile_picture": self.image
#         }
#         response = self.client.post(url, data, format="multipart")  # Ensure 'multipart' format for file upload
#         self.assertEqual(status.HTTP_201_CREATED, response.status_code)

#         # Validate the response contains expected data
#         self.assertIn("msg", response.data)
#         self.assertEqual(response.data["msg"], "User Info added successfully")

#     def test_getuser(self):
#         AddUserInfo.objects.create(user=self.user, bio="This is a test bio")
#         url = reverse('userinfo')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("user info", response.data)