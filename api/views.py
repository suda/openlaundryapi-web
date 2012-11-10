# -*- coding: utf-8 -*-

import logging
import simplejson as json

import numpy as np
from django.http import HttpResponse

from devices.models import Device


logger = logging.getLogger(__name__)


def json_response(data):
    data = json.dumps(data)
    response = HttpResponse(data)
    response['Content-Type'] = 'application/json'
    return response


def collect_data(request):
    try:
        data = json.loads(request.body)
        device_id = data['device_id']
        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            device = Device.objects.create(device_id=device_id, name=device_id)
        logger.info('Incoming data from device: %s', device)
        timestamp_start = long(data['timestamp_start'])
        samples = np.array([int(d) for d in data['data']])
        timestamp_end = long(data['timestamp_end'])
        logger.info('Received %s samples from %s to %s', len(samples), timestamp_start, timestamp_end)
    except Exception as e:
        return json_response({
            'status': 'ERROR',
            'message': str(e),
        })
    return json_response({
        'status': 'OK',
    })
