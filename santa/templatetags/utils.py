# -*- coding: utf-8 -*-
import urllib

from django.http import HttpRequest
from django.core.urlresolvers import reverse
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_full_url(context, view_name, *args):
    path = reverse(view_name, args=args)
    return context.request.build_absolute_uri(path)
