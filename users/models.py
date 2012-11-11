
from datetime import datetime
import hashlib
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from devices.models import Device


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=40, unique=True)
    debug = models.BooleanField(default=False)


def create_profile(sender, instance, created, **kwargs):
    u"""
    Automatic profile creation when a User instance is created.
    """
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        profile.token = hashlib.sha1("%s%s" % (datetime.now(), instance.username)).hexdigest()
        profile.save()


def create_device(sender, instance, created, **kwargs):
    if created:
        device_id = hashlib.sha1("%s" % instance.id).hexdigest()
        device = Device.objects.create(user=instance, device_id=device_id, name="%s's device" % instance.username)
        device.save()


post_save.connect(create_profile, sender=User, dispatch_uid='users.models.create_profile')
post_save.connect(create_device, sender=User, dispatch_uid='users.models.create_device')
