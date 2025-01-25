from django.urls import path, include
# from .views import blog_all
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('blog',views.Blog_all,basename='blog')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

