# -*- coding: utf-8 -*-

import os
import logging
import simplejson as json
import datetime
import time
import math

import numpy as np

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from devices.models import Device, Wash
from users.models import UserProfile


logger = logging.getLogger(__name__)


def json_response(data):
    data = json.dumps(data)
    response = HttpResponse(data)
    response['Content-Type'] = 'application/json'
    return response


@csrf_exempt
def collect_data(request, device_id, token):
    profile = get_object_or_404(UserProfile, token=token)
    logger.debug(request.body)
    try:
        data = json.loads(request.body)

        # find device
        try:
            device = Device.objects.get(device_id=device_id, user=profile.user)
        except Device.DoesNotExist:
            device = Device.objects.create(device_id=device_id, name=device_id, user=profile.user)
        wash = device.get_latest_wash()

        logger.info('Incoming data from device: %s', device)
        timestamp_start = long(data['timestamp_start'])
        samples = np.array([int(d) for d in data['data']])
        timestamp_end = long(data['timestamp_end'])
        logger.info('Received %s samples from %s to %s', len(samples), timestamp_start, timestamp_end)
        logger.info('Writing samples to file: %s', wash.data_file)
        wash.write_samples(samples)

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
def set_status(request, device_id, token):
    profile = get_object_or_404(UserProfile, token=token)
    device = get_object_or_404(Device, device_id=device_id, user=profile.user)
    old_status = device.status
    new_status = old_status
    try:
        data = json.loads(request.body)
        device.status = data['status']
        new_status = device.status
        device.save()
    except Exception as e:
        logger.exception(u"Set status error")
        return json_response({
            'status': 'ERROR',
            'message': str(e),
        })
    return json_response({
        'device_id': device.device_id,
        'status': 'OK',
        'old_status': old_status,
        'new_status': new_status,
    })


@csrf_exempt
def device_status(request, device_id):
    device = get_object_or_404(Device, device_id=device_id)
    user_profile = device.user.get_profile()

    programs = [
        { 'progress': 0, 'program': 'A' },
        { 'progress': 20, 'program': 'B' },
        { 'progress': 45, 'program': 'C' },
        { 'progress': 70, 'program': 'D' },
        { 'progress': 75, 'program': 'E' },
        { 'progress': 85, 'program': 'F' },
    ]

    if user_profile.debug:
        interval = 60 * 10
        timestamp = time.mktime(datetime.datetime.now().timetuple())
        progress = timestamp / interval
        time_start = interval * math.floor(progress)
        progress = progress - math.floor(progress)
        print progress

        current_program = ''
        for program in programs:
            if progress * 100 > program['progress']:
                current_program = program['program']

        status = 'WORKING'
        if progress * 100 > 90:
            current_program = None
            status = 'IDLE'

        response_dict = {
            'device_id': device.device_id,
            'name': device.name,
            'status': status,
            'program': current_program,
            'time_started': None if status == 'IDLE' else datetime.datetime.fromtimestamp(time_start).isoformat(),
            'time_remaining': None if status == 'IDLE' else str(datetime.timedelta(seconds=(interval - (interval * progress)))),
            'progress': None if status == 'IDLE' else str(int(progress * 100))
        }

    else:
        response_dict = {
            'device_id': device.device_id,
            'name': device.name,
            'status': device.status,
            'program': '',
            'progress': 0
        }
        wash = device.get_latest_wash()
        if device.status in ['WORKING', 'PAUSED']:
            response_dict['time_started'] = str(wash.created)
            response_dict['time_remaining'] = '00:00:00'

    return json_response(response_dict)
