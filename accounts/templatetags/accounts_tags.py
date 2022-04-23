from django import template


register = template.Library()


@register.filter(name="as_percentage_of")
def as_percentage_of(number, percentage):
    try:
        return (float(number) * percentage) / 100
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter(name="subtract")
def subtract(number1, number2):
    try:
        return number1 - number2
    except (ValueError, ZeroDivisionError):
        return "Error"
