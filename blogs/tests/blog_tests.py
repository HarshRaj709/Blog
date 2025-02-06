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
def client():
    return APIClient()


@pytest.fixture
def user(db):
    user = User.objects.create(username='Paneer', password='pass123')
    user_info = AddUserInfo.objects.create(user=user, bio='kala katha')
    return user


@pytest.fixture
def refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return refresh


@pytest.fixture
def authenticated_user(client,refresh_token):
    client.credentials(HTTP_AUTHORIZATION = f'Bearer {refresh_token.access_token}')
    return client


@pytest.fixture
def category_setup(db):
    category = Category.objects.create(category_name='Tech')
    return category


@pytest.fixture
def blog_setup(user,category_setup):
    blog = Blog.objects.create(title="Mera Bdla", content="Mera Bdla content", category=category_setup, writer=user)
    return blog


@pytest.fixture
def image_setup():
    with open('/home/savera/Downloads/PHOTO.jpeg','rb') as f:
        image_data = f.read()
    image = SimpleUploadedFile(name='image.jpg', content=image_data, content_type='image/jpeg')
    return image
    


class TestBlog:
    def test_blogs(self,client,blog_setup):
        url = reverse('blogs_get')
        response =client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['title'] == "Mera Bdla"



    @patch("rest_framework.test.APIClient.get")
    def test_mocked_blog(self, mock_get, client):
        mock_data = {
            'id': 1, 'writer': 'mock_writer', 'title': 'First_mocked',
            'content': 'Mocked content', 'category': 1, 'category_name': 'mocked category'
        }
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.data = mock_data

        url = reverse('blogs_get')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['writer'] == 'mock_writer'


    @pytest.mark.slow
    def test_create_blog(self,authenticated_user,user,category_setup,image_setup):
        url = reverse('create')
        data = {"writer":user,"title": "Mera Bdla", "content": "Mera Bdla content","category": category_setup.id, "content_image":image_setup}
        response = authenticated_user.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED


    def test_update_blog(self, blog_setup,authenticated_user):
        url = reverse('update', args=[blog_setup.id])
        data = {'title': 'changed'}
        response = authenticated_user.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'changed'


    def test_delete_blog(self,blog_setup, authenticated_user):
        url = reverse('delete', args=[blog_setup.id])
        response = authenticated_user.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


    def test_get_user_blogs(self, authenticated_user):
        url = reverse('Userblog')
        response = authenticated_user.get(url)
        assert response.status_code == status.HTTP_200_OK


    def test_create_blog_category(self, authenticated_user):
        url = reverse('categories')
        data = {'category_name': 'Health'}
        response = authenticated_user.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'Health' in response.data['message'] 


    def test_get_user_info(self,user,blog_setup,authenticated_user):
        url = reverse('userinfo')
        response = authenticated_user.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'user info' in response.data
        assert response.data['blogs'][0]['title'] == 'Mera Bdla'

    def test_add_user_info(self, user,authenticated_user):
        url = reverse('adduserinfo')
        data = {'user': user, 'bio': 'Updated Bio'}
        response = authenticated_user.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'Paneer' in response.data['msg']
