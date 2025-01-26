from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class AddUserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    category_name = models.CharField(max_length=500)

class Blog(models.Model):
    writer = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='blog',blank=True,null=True)
    content_image = models.ImageField(upload_to='content_image',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title