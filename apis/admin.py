from django.contrib import admin
from .models import Blog,AddUserInfo

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Blog._meta.fields]

@admin.register(AddUserInfo)
class AddUserInfo(admin.ModelAdmin):
    list_display = [field.name for field in AddUserInfo._meta.fields]
