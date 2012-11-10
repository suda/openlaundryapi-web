# -*- coding: utf-8 -*-

import os
import logging
import simplejson as json

import numpy as np
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from devices.models import Device, Wash


logger = logging.getLogger(__name__)


def json_response(data):
    data = json.dumps(data)
    response = HttpResponse(data)
    response['Content-Type'] = 'application/json'
    return response


@csrf_exempt
def collect_data(request):
    try:
        data = json.loads(request.body)
        device_id = data['device_id']

        # find device
        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            device = Device.objects.create(device_id=device_id, name=device_id)

        # find latest wash
        try:
            wash = device.washes.latest()
        except Wash.DoesNotExist:
            wash = Wash.objects.create(device=device)
            filename = '%d.wash.npy' % wash.id
            wash.data_file = os.path.join(settings.WASH_DATA_ROOT, filename)
            wash.save()

        logger.info('Incoming data from device: %s', device)
        timestamp_start = long(data['timestamp_start'])
        samples = np.array([int(d) for d in data['data']])
        timestamp_end = long(data['timestamp_end'])
        logger.info('Received %s samples from %s to %s', len(samples), timestamp_start, timestamp_end)
        logger.info('Writing samples to file: %s', wash.data_file)
        if os.path.exists(wash.data_file):
            existing_data = np.load(wash.data_file)
            samples = np.append(existing_data, samples)
        np.save(wash.data_file, samples)

    except Exception as e:
        logger.exception(u"Collect data error")
        return json_response({
            'status': 'ERROR',
            'message': str(e),
        })
    return json_response({
        'device_id': device.device_id,
        'wash_id': wash.id,
        'status': 'OK',
    })


@csrf_exempt
def device_status(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    return json_response({
        'device_id': device.device_id,
        'name': device.name,
        'status': 'FINISHED',
    })
