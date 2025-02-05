import pytest
from blogs.models import Blog,Category
from authentication.models import AddUserInfo
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

#Mocking
from unittest.mock import patch

User = get_user_model()


@pytest.mark.django_db
class TestBlog:
    @pytest.fixture(autouse=True,scope="function")      #runs each time the function executes
    # @pytest.fixture(autouse=True,scope="module")        # causing error as in this only single time fixture is running
    # @pytest.fixture(autouse=True,scope="class")         # causing error as in this only single time fixture is running, use this when no database interaction is happening within class, or expensive setup.
    # @pytest.fixture(autouse=True,scope="session")         # causing error as in this only single time fixture is running, use this when no database interaction is happening within class, or expensive setup.
    def setup(self,db):
        """THis is Docstring for blog testing Fixtures"""
        self.client = APIClient()
        self.category = Category.objects.create(category_name='name')
        self.user = User.objects.create(username='Paneer',password='pass123')
        self.blog = Blog.objects.create(title="Mera Bdla",content="Mera Bdla content",category=self.category,writer=self.user)
        self.refresh = RefreshToken.for_user(self.user)
        self.UserInfo = AddUserInfo.objects.create(user = self.user,bio='kala katha')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}")
        with open('/home/savera/Downloads/PHOTO.jpeg', 'rb')as image:
            image_data = image.read()
        self.image = SimpleUploadedFile(name='image.jpg', content=image_data, content_type='image/jpeg')
        # yield
        # print('Execution Complete')



    # def test_blog(self):
    #     url = reverse('Blogs_get')
    #     response = self.client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data)>0
    #     print(response.data)


#Mocking in pytest
    @patch("rest_framework.test.APIClient.get")
    def test_blog(self,mock_get):       #The mock_get parameter is automatically injected by the @patch decorator. it replace real client.get with the mocked one.
        mock_data = {
            'id': 1, 'writer': 'mock_writer', 'title': 'First_mocked', 'content': 'Mocked content', 'category': 1, 'category_name': 'mocked category'
        }
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.data = mock_data

        url = reverse('blogs_get')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['writer'] == 'mock_writer'
        print(response.data)

    
    @pytest.mark.slow           #Marked with slow
    def test_blogcreate(self):
        url = reverse('create')
        data = {"title":"Mera Bdla","content":"Mera Bdla content","category":self.category.id,"content_image":self.image}
        response = self.client.post(url,data)
        assert response.status_code == status.HTTP_201_CREATED
        print('Slow Run')
        

    def test_blogupdate(self):
        url = reverse('update',args=[self.blog.id])
        data = {'title':'changed'}
        response = self.client.patch(url,data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'changed'
        # print(response.data['title'])

    def test_blogdelete(self):
        url=reverse('delete',args = [self.blog.id])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_blogUser(self):
        url = reverse('Userblog')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        #print(response.data)

    def test_blogcategory(self):
        url =reverse('categories')
        data = {'category_name':'Tech'}
        response = self.client.post(url,data)
        #print(response.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_userinfo(self):
        url = reverse('userinfo')
        response = self.client.get(url)
        # print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert 'user info' in response.data 

    def test_userinfopost(self):
        url = reverse('adduserinfo')
        data = {'user':self.user,'bio':'kala katha nhi'}
        response = self.client.post(url,data)
        assert response.status_code == status.HTTP_201_CREATED

    

    def divide(self,x, y):
        return x / y  # This will raise ZeroDivisionError if y=0

    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):  # Expects an exception
            self.divide(10, 30)                 #self = <blog_tests.TestBlog object at 0x7c7357a9ae40>

    def test_divide_by_zero(self):
       with pytest.raises(ZeroDivisionError):  # Expects an exception
            self.divide(10,0)                     # E       Failed: DID NOT RAISE <class 'ZeroDivisionError'>

                                                    # blogs/tests/blog_tests.py:89: Failed
