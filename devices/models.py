# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import PassThroughManager
from model_utils.models import TimeStampedModel
from model_utils.fields import MonitorField, StatusField
from model_utils import Choices


class DeviceQuerySet(QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class Device(TimeStampedModel):
    STATUS = Choices('IDLE', 'PAUSED', 'WORKING', 'LEARNING')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_(u"Device owner"), related_name='devices')
    device_id = models.CharField(max_length=50, verbose_name=_(u"Device ID"))
    name = models.CharField(max_length=100, verbose_name=_(u"Device name"))

    status = StatusField()
    status_changed = MonitorField(monitor='status')

    objects = PassThroughManager.for_queryset_class(DeviceQuerySet)()

    class Meta:
        verbose_name = _(u"Device")
        verbose_name_plural = _(u"Devices")
        ordering = ['-created']

    def __unicode__(self):
        return self.name

    def get_latest_wash(self):
        try:
            wash = self.washes.latest()
        except Wash.DoesNotExist:
            wash = Wash.objects.create(device=self)
            filename = '%d.wash.npy' % wash.id
            wash.data_file = os.path.join(settings.WASH_DATA_ROOT, filename)
            wash.save()
        return wash


class Wash(TimeStampedModel):
    device = models.ForeignKey(Device, verbose_name=_(u"Device"), related_name='washes')
    data_file = models.CharField(max_length=200, blank=True, default='', verbose_name=_(u"Data file"))

    class Meta:
        verbose_name = _(u"Wash")
        verbose_name_plural = _(u"Washes")
        ordering = ['-modified']
        get_latest_by = 'modified'

    def __unicode__(self):
        return u"%s - wash %d" % (self.device.name, self.id)
