from django import template
from catalog.models import Course
from django.contrib.auth.models import User
import time

register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def show_top_menu(context):
    res = Course.objects.first()
    if res:
        return {'res': res.course}
    else:
        return {'res': 2.6}



