# -*- coding: utf-8 -*-

import re

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def active_nav_item(context, caption, regexp, url_name, *args, **kwargs):
    request = context['request']
    url = reverse(url_name, args=args, kwargs=kwargs)
    return mark_safe('<li%s><a href="%s">%s</a></li>') % (
        ' class="active"' if re.search(regexp, request.path) else '',
        url,
        caption,
    )

