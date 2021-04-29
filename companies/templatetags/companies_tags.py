from django import template
from django.utils.safestring import mark_safe
from pprint import pp


register = template.Library()

@register.filter(name='addstr')
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    concatinated = str(arg1) + str(arg2)
    return mark_safe(concatinated)

@register.filter(name='dir')
def addstr(arg1):
    return dir(arg1)