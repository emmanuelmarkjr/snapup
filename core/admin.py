# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from accounts.models import SnapLink

# Register your models here.


class SnapLinkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SnapLink._meta.fields if field.name != "id"]
    search_fields = ('price', 'user', 'snap_link')
    list_filter = ("date_added", "time_added", "notify_me_type", "percentage")
admin.site.register(SnapLink, SnapLinkAdmin)

