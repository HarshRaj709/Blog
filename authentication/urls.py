from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('registration/',views.UserRegistrationView.as_view(),name='register'),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('logout/',views.LogoutUser.as_view(),name='logout'),
    path('password_reset/',views.Password_Reset.as_view(),name='Password_Reset'),
    path('reset/<str:uidb64>/<str:token>/', views.ResetPasswordAPIView.as_view(), name='password_reset_confirm'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

    