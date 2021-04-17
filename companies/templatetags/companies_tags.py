from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(name='addstr')
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    concatinated = str(arg1) + str(arg2)
    return mark_safe(concatinated)
