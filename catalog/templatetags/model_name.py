from django import template
register = template.Library()
from catalog.models import MobTel, Television

@register.simple_tag
def get_verbose_field_name(instance):
    """
    Returns verbose_name for a field.

    """
    print()
    print(instance)
    print()
    print()
    print()
    if instance == 'television':
        r = [i.verbose_name.title() for i in Television._meta.get_fields()]
        print(r)
        return r[7:]
