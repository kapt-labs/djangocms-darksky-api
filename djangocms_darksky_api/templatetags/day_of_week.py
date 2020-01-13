import datetime
from django.utils.translation import ugettext_lazy as _
from django import template

register = template.Library()


@register.filter
def dayofweek(timestamp):
    return _(datetime.datetime.fromtimestamp(timestamp).strftime("%A"))
