# -*- coding: utf-8 -*-

import simplejson as json

from django.http import HttpResponse


def json_response(data):
    data = json.dumps(data)
    response = HttpResponse(data)
    response['Content-Type'] = 'application/json'
    return response


def collect_data(request):
    return json_response({
        'status': 'OK',
    })
