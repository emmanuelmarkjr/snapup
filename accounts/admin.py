# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from accounts.models import UserProfile

from django.contrib import admin

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields if field.name != "id"]

admin.site.register(UserProfile, UserProfileAdmin)