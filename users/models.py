
import hashlib
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=40)
    debug = models.BooleanField(default=False)


def create_profile(sender, instance, created, **kwargs):
    u"""
    Automatic profile creation when a User instance is created.
    """
    if created:
        profile = UserProfile.objects.get_or_create(user=instance)
        profile.token = hashlib.sha1("%s%s" % (datetime.now(), user.username)).hexdigest()
        profile.save()


post_save.connect(create_profile, sender=User, dispatch_uid='users.models.create_profile')
