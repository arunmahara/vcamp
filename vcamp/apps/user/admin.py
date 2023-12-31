from django.contrib import admin
from .models import User, FCMDevice, Recipe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'created_at']
    search_fields = ['email']


@admin.register(FCMDevice)
class FCMDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'fcm_token']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "ingredients"]