import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from blogs.models import Blog, Category
from authentication.models import AddUserInfo

# Mocking
from unittest.mock import patch

User = get_user_model()


@pytest.fixture
def setup_test_data(db):
    client = APIClient()
    user = User.objects.create(username='Paneer', password='pass123')
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    category = Category.objects.create(category_name='Tech')
    blog = Blog.objects.create(title="Mera Bdla", content="Mera Bdla content", category=category, writer=user)
    user_info = AddUserInfo.objects.create(user=user, bio='kala katha')
    with open('/home/savera/Downloads/PHOTO.jpeg', 'rb') as image:
        image_data = image.read()
    image = SimpleUploadedFile(name='image.jpg', content=image_data, content_type='image/jpeg')

    return {
        "client": client,
        "user": user,
        "refresh": refresh,
        "category": category,
        "blog": blog,
        "user_info": user_info,
        "image": image
    }
    


class TestBlog:
    def test_blogs(self,setup_test_data):
        url = reverse('blogs_get')
        response =setup_test_data['client'].get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['title'] == "Mera Bdla"



    @patch("rest_framework.test.APIClient.get")
    def test_mocked_blog(self, mock_get, setup_test_data):
        mock_data = {
            'id': 1, 'writer': 'mock_writer', 'title': 'First_mocked',
            'content': 'Mocked content', 'category': 1, 'category_name': 'mocked category'
        }
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.data = mock_data

        url = reverse('blogs_get')
        response = setup_test_data["client"].get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['writer'] == 'mock_writer'

    @pytest.mark.slow
    def test_create_blog(self, setup_test_data):
        url = reverse('create')
        data = {"writer":setup_test_data['user'],"title": "Mera Bdla", "content": "Mera Bdla content","category": setup_test_data["category"].id, "content_image": setup_test_data["image"]}
        response = setup_test_data["client"].post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_blog(self, setup_test_data):
        url = reverse('update', args=[setup_test_data["blog"].id])
        data = {'title': 'changed'}
        response = setup_test_data["client"].patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'changed'

    def test_delete_blog(self, setup_test_data):
        url = reverse('delete', args=[setup_test_data["blog"].id])
        response = setup_test_data["client"].delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_user_blogs(self, setup_test_data):
        url = reverse('Userblog')
        response = setup_test_data["client"].get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_blog_category(self, setup_test_data):
        url = reverse('categories')
        data = {'category_name': 'Health'}
        response = setup_test_data["client"].post(url, data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_get_user_info(self, setup_test_data):
        url = reverse('userinfo')
        response = setup_test_data["client"].get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'user info' in response.data

    def test_add_user_info(self, setup_test_data):
        url = reverse('adduserinfo')
        data = {'user': setup_test_data["user"], 'bio': 'Updated Bio'}
        response = setup_test_data["client"].post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
