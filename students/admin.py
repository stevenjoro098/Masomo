from django.contrib import admin
from .models import Profile


# Register your models here.
@admin.register(Profile)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ['user', 'telephone', 'image']
