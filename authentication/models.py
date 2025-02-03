from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.
class AddUserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    failed_login_attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username