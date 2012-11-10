
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=40)
    debug = models.BooleanField(default=False)

