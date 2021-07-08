from django import template
from django.utils.safestring import mark_safe
from pprint import pp
import json


register = template.Library()


@register.filter(name='addstr')
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    concatinated = str(arg1) + str(arg2)
    return mark_safe(concatinated)

@register.filter(name='convert_to_JSON')
def convert_obj_to_JSON(obj):
    """converts python object to JSON string"""
    return json.dumps(obj)

@register.filter('dir')
def get_dir(obj):
    attrs = {}
    for attr in dir(obj):
        attrs[attr] = str(getattr(obj, attr, None))
    response = json.dumps(attrs, indent=4)
    return response


@register.filter(name='get_attr')
def get_nested_attr(obj, attr, default=None, attr_split_on='.'):
    """Filter tag to get python object's attributes.
    Supportes nested attributes separated by '.'.
    If attribute doesn't exists returns None as default.
    """
    attrs = attr.split(attr_split_on)
    value = obj
    for attr in attrs:
        if hasattr(value, 'get'):
            value = value.get(attr, default)
        else:
            value = getattr(value, attr, default)
    return value

@register.filter(name='get_field')
def get_field(form, field_name):
    return form[field_name]
