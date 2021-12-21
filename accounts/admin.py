from re import search
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

# Register your models here.
# class UserAdminConfig(UserAdmin):
#     search_fields = ('email','username',)
#     list_filter = ('is_staff','is_active',)
#     ordering = ('-date_joined',)
#     list_display = ('username','email','is_staff','is_active')
admin.site.register(User)