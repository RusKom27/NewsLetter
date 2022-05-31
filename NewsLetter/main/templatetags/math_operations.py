import datetime
from django import template

register = template.Library()


@register.simple_tag()
def post_date(date_created):
    return datetime.datetime.now() - date_created


