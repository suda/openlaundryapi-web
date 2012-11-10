# -*- coding: utf-8 -*-

import os
import logging
import simplejson as json

import numpy as np
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from devices.models import Device


logger = logging.getLogger(__name__)
# TODO: data file per each wash
data_file = 'data.npy'


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
        try:
            device = Device.objects.get(device_id=device_id)
        except Device.DoesNotExist:
            device = Device.objects.create(device_id=device_id, name=device_id)
        logger.info('Incoming data from device: %s', device)
        timestamp_start = long(data['timestamp_start'])
        samples = np.array([int(d) for d in data['data']])
        timestamp_end = long(data['timestamp_end'])
        logger.info('Received %s samples from %s to %s', len(samples), timestamp_start, timestamp_end)
        if os.path.exists(data_file):
            existing_data = np.load(data_file)
            samples = np.append(existing_data, samples)
        np.save(data_file, samples)

    except Exception as e:
        return json_response({
            'status': 'ERROR',
            'message': str(e),
        })
    return json_response({
        'status': 'OK',
    })
