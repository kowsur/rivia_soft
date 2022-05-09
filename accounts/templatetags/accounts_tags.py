from django import template


register = template.Library()


@register.filter(name="as_percentage_of")
def as_percentage_of(number, percentage):
    try:
        return (float(number) * percentage) / 100
    except (ValueError, ZeroDivisionError):
        return 0
    except (Exception):
        return "Error"

@register.filter(name="subtract")
def subtract(number1, number2):
    try:
        return float(number1) - float(number2)
    except Exception:
        return "Error"

@register.filter(name="add")
def add(number1, number2):
    try:
        return float(number1) + float(number2)
    except Exception:
        return "Error"
