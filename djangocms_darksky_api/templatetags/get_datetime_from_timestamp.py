import datetime
from django import template

register = template.Library()


@register.filter
def get_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)
