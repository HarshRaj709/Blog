from django.contrib import admin
from .models import AddUserInfo

# Register your models here.
@admin.register(AddUserInfo)
class AddUserInfo(admin.ModelAdmin):
    list_display = [field.name for field in AddUserInfo._meta.fields]