# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Device


class DeviceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Device, DeviceAdmin)
