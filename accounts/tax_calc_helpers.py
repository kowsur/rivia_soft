from dataclasses import dataclass


@dataclass
class Tax:
    applied_on: float
    rate: float
    amount: float

@dataclass
class Tax_ReturnType:
    total: float
    details: list[Tax]


def percentage_of(number, percent):
    return (number*percent)/100


def get_personal_allowance_reduction(total_income, personal_allowance, personal_allowance_limit, one_unit_deducted_from_PA_earned_over_PAL):
    personal_allowance_reduction = 0
    if (total_income>=personal_allowance_limit):
        personal_allowance_reduction = (total_income - personal_allowance_limit)/one_unit_deducted_from_PA_earned_over_PAL
        if (personal_allowance_reduction>personal_allowance):
            personal_allowance_reduction = personal_allowance
    return personal_allowance_reduction


def uk_tax(
    total_income,
    personal_allowance = 12570,
    basic_rate_max = 37700,
    higher_rate_max = 150000,
    basic_tax_rate = 20,
    higher_tax_rate = 40,
    additional_tax_rate = 45,
    personal_allowance_limit = 100000,
    one_pound_reduction_from_PA_earned_over_PAL = 2
)->Tax_ReturnType:
    personal_allowance-=get_personal_allowance_reduction(total_income, personal_allowance, personal_allowance_limit, one_pound_reduction_from_PA_earned_over_PAL)

    if total_income>personal_allowance:
        total_income = total_income-personal_allowance
    else:
        total_income = 0

    basic_rate_applied_on = 0
    basic_rate_tax_amount = 0
    higher_rate_applied_on = 0
    higher_rate_tax_amount = 0
    additional_rate_applied_on = 0
    additional_rate_tax_amount = 0
    total_tax = 0

    if total_income>higher_rate_max:
        basic_rate_applied_on = basic_rate_max
        basic_rate_tax_amount = percentage_of(basic_rate_applied_on, basic_tax_rate)

        higher_rate_applied_on = higher_rate_max - basic_rate_max
        higher_rate_tax_amount = percentage_of(higher_rate_applied_on, higher_tax_rate)

        additional_rate_applied_on = total_income - higher_rate_max
        additional_rate_tax_amount = percentage_of(additional_rate_applied_on, additional_tax_rate)

    elif total_income>basic_rate_max:
        basic_rate_applied_on = basic_rate_max
        basic_rate_tax_amount = percentage_of(basic_rate_max, basic_tax_rate)

        higher_rate_applied_on = total_income - basic_rate_max
        higher_rate_tax_amount = percentage_of(higher_rate_applied_on, higher_tax_rate)

    elif total_income>0:
        basic_rate_applied_on = total_income
        basic_rate_tax_amount = percentage_of(basic_rate_applied_on, basic_tax_rate)
    
    total_tax = basic_rate_tax_amount + higher_rate_tax_amount + additional_rate_tax_amount
    details = [
            Tax(basic_rate_applied_on, basic_tax_rate, basic_rate_tax_amount),
            Tax(higher_rate_applied_on, higher_tax_rate, higher_rate_tax_amount),
            Tax(additional_rate_applied_on, additional_tax_rate, additional_rate_tax_amount),
        ]

    return Tax_ReturnType(total=total_tax, details=details)


def uk_class_4_tax(
    total_income: float = 0,
    basic_rate_start: float = 9569,
    higher_rate_start: float = 50270,
    basic_rate_tax_percentage: float = 9,
    higher_rate_tax_percentage: float = 2,
):
    basic_rate_applied_on = 0
    basic_rate_tax_amount = 0
    higher_rate_applied_on = 0
    higher_rate_tax_amount = 0
    
    total_tax = 0

    if basic_rate_start<=total_income<=higher_rate_start:
        basic_rate_applied_on = total_income - basic_rate_start
        basic_rate_tax_amount = percentage_of(basic_rate_applied_on, basic_rate_tax_percentage)

    elif total_income>higher_rate_start:
        basic_rate_applied_on = higher_rate_start - basic_rate_start
        basic_rate_tax_amount = percentage_of(basic_rate_applied_on, basic_rate_tax_percentage)

        higher_rate_applied_on = total_income - higher_rate_start
        higher_rate_tax_amount = percentage_of(higher_rate_applied_on, higher_rate_tax_percentage)

    total_tax = higher_rate_tax_amount + basic_rate_tax_amount
    details = [
        Tax(basic_rate_applied_on, basic_rate_tax_percentage, basic_rate_tax_amount),
        Tax(higher_rate_applied_on, higher_rate_tax_percentage, higher_rate_tax_amount),
    ]

    return Tax_ReturnType(total=total_tax, details=details)
