# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView

from .models import Device


class DeviceListView(ListView):
    queryset = Device.objects.all()
    context_object_name = 'devices'
    paginate_by = 10


class DeviceDetailView(DetailView):
    model = Device
    context_object_name = 'device'
    slug_field = slug_url_kwarg = 'device_id'
    template_name = "devices/device.html"

