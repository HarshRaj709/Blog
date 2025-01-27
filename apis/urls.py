from django.urls import path, include
# from .views import blog_all
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

# router = DefaultRouter()
# router.register('blog',views.Blog_all,basename='blog')

urlpatterns = [
    # path('', include(router.urls)),
    path('registration/',views.UserRegistrationView.as_view(),name='register'),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('logout/',views.LogoutUser.as_view(),name='logout'),
    path('Blogs/',views.Listofall.as_view(),name='Blogs_get'),
    path('create/',views.CreateBlog.as_view(),name='create'),
    path('Blogs/<int:pk>/update/',views.UpdateBlog.as_view(),name='update'),
    path('delete/<int:pk>/',views.DeleteBlog.as_view(),name='delete'),
    path('userblog/',views.UserBlog.as_view(),name='Userblog'),
    path('blog_cat/',views.CategoryView.as_view(),name='categories'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('adduserinfo/',views.UserInfoViews.as_view(),name='adduserinfo'),
    path('userinfo/',views.GetUserInfo.as_view(),name='userinfo'),
]

