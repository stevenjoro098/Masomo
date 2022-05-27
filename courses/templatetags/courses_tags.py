from django import template
from ..models import Topics

register = template.Library()


@register.simple_tag
def units_id():
    return Topics.objects.filter()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
