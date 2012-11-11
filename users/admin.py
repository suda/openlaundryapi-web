from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'token', 'debug')


admin.site.register(UserProfile, UserProfileAdmin)
