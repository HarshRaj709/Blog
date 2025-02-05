from django.urls import path, include
from . import views

urlpatterns = [
    path('blogs/',views.Listofall.as_view(),name='blogs_get'),      #naming conventions
    path('create/',views.CreateBlog.as_view(),name='create'),
    path('<int:pk>/update/',views.UpdateBlog.as_view(),name='update'),
    path('delete/<int:pk>/',views.DeleteBlog.as_view(),name='delete'),
    path('userblog/',views.UserBlog.as_view(),name='Userblog'),
    path('blog_cat/',views.CategoryView.as_view(),name='categories'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('adduserinfo/',views.UserInfoViews.as_view(),name='adduserinfo'),
    path('userinfo/',views.GetUserInfo.as_view(),name='userinfo'),
    ]

# need to block both tokens after logout            (not good to do that)
# need to use pytest for testing                            (done)
# need to remove PasswordResetForm and use api for that.        (done)
# make changes so that user dont need to send refresh token from frontend, use access token to 
                    # get refresh token         (not possible to generate refresh token from access token)
# need to refactor all the blog, user, authentication code into different apps (done)