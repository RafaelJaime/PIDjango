from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from . import forms
# Register your models here.

admin.site.register(User, UserAdmin)