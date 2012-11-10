# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Device, Wash


class DeviceAdmin(admin.ModelAdmin):
    pass


class WashAdmin(admin.ModelAdmin):
    pass


admin.site.register(Device, DeviceAdmin)
admin.site.register(Wash, WashAdmin)
