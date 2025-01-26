from django.urls import path, include
# from .views import blog_all
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register('blog',views.Blog_all,basename='blog')

urlpatterns = [
    # path('', include(router.urls)),
    path('registration/',views.UserRegistrationView.as_view(),name='register'),
]

