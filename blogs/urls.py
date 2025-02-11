from django.urls import path, include
from . import views

urlpatterns = [
    path('blogs/',views.Listofall.as_view(),name='blogs_get'),      
    path('create/',views.CreateBlog.as_view(),name='create'),
    path('<int:pk>/update/',views.UpdateBlog.as_view(),name='update'),
    path('delete/<int:pk>/',views.DeleteBlog.as_view(),name='delete'),
    path('userblog/',views.UserBlog.as_view(),name='Userblog'),
    path('blog_cat/',views.CategoryView.as_view(),name='categories'),
    path('adduserinfo/',views.UserInfoViews.as_view(),name='adduserinfo'),
    path('userinfo/',views.GetUserInfo.as_view(),name='userinfo'),
    ]

