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


def calculate_capital_allowance(amount, allowance_percentage, personal_usage_percentage):
    allowance = (amount*allowance_percentage)/100
    personal_usage = (allowance*personal_usage_percentage)/100
    return allowance - personal_usage

register.filter("calculate_capital_allowance", calculate_capital_allowance)