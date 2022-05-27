from django import template
from courses.models import Unit

register = template.Library()


@register.filter(name='user_info')
def user_info(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='user_enrolled')
def user_enrolled(user, unit_id):
    unit = Unit.objects.get(id=unit_id)
    enrolled = unit.students.get(username=user.username)
    if user.username == enrolled:
        return True
    else:
        return False
