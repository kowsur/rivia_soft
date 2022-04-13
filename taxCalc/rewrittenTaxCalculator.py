from dataclasses import dataclass


@dataclass
class TaxedIncomeUKTax:
    total_income: float|int = 0
    basic_tax: float|int = 0
    higher_tax: float|int = 0
    additional_tax: float|int = 0
    personal_allowance_reduction: int|float = 0
    
    @property
    def total_tax(self):
        return self.basic_tax + self.higher_tax + self.additional_tax

    def __str__(self) -> str:
        return f"UK Tax\n" +\
            f"Total income {self.total_income}\n" +\
            f"Personal Allowance Reduced by {self.personal_allowance_reduction}\n" +\
            f"Basic rate tax applied {self.basic_tax}\n" +\
            f"Higher rate tax applied {self.higher_tax}\n" +\
            f"Additional rate tax applied {self.additional_tax}\n" +\
            f"Total Tax {self.total_tax}\n"

@dataclass
class TaxedIncomeUKClass4:
    self_employment_net_income: int|float = 0
    other_income: int|float = 0
    class_4_basic_rate_tax: float|int = 0
    class_4_higher_rate_tax: float|int = 0
    
    @property
    def total_income(self):
        return self.other_income + self.self_employment_net_income

    @property
    def total_tax(self):
        return self.class_4_higher_rate_tax + self.class_4_basic_rate_tax
    
    def __str__(self) -> str:
        return f"Calss 4 Tax\n" +\
            f"Total income {self.total_income}\n" +\
            f"Basic rate tax applied {self.class_4_basic_rate_tax}\n" +\
            f"Higher rate tax applied {self.class_4_higher_rate_tax}\n" +\
            f"Total Tax {self.total_tax}\n"


@dataclass
class TaxedIncomeUKClass2:
    self_employment_net_income: int|float = 0
    other_income: int|float = 0
    tax_applied: int|float = 158.6
    
    @property
    def total_income(self):
        return self.other_income + self.self_employment_net_income

    @property
    def total_tax(self):
        return self.tax_applied

    def __str__(self) -> str:
        return f"Calss 2 Tax\n" +\
            f"Total income {self.total_income}\n" +\
            f"Higher rate tax applied {self.tax_applied}\n" +\
            f"Total Tax {self.total_tax}\n"



def uk_tax(
    income, # selfemp net profit + (other taxable incomes - total of )
    personal_allowance = 12570,
    basic_rate_max = 37700,
    higher_rate_max = 150000,
    basic_rate_tax = 20/100,
    higher_rate_tax = 40/100,
    additional_rate = 45/100,
    personal_allowance_limit = 100000,
    one_unit_deducted_from_personal_allowance_earned_over_PAL = 2
):
    # employment_income = 0
    # selfemployment_net_prfit = 0
    # other_income_grant = 106000
    # total_income = employment_income + selfemployment_net_prfit + other_income_grant
    total_income = income

    personal_allowance_reduction = 0
    if (total_income>=personal_allowance_limit):
        personal_allowance_reduction = (total_income - personal_allowance_limit)/one_unit_deducted_from_personal_allowance_earned_over_PAL
        if (personal_allowance_reduction>personal_allowance):
            personal_allowance_reduction = personal_allowance

    personal_allowance-=personal_allowance_reduction

    taxable_income = 0
    if total_income>personal_allowance:
        taxable_income = total_income-personal_allowance

    basic_rate_tax_applied = 0
    higher_rate_tax_applied = 0
    additional_rate_tax_applied = 0
    total_tax = 0

    if taxable_income>higher_rate_max:
        basic_rate_tax_applied = basic_rate_max*basic_rate_tax
        higher_rate_tax_applied = (higher_rate_max - basic_rate_max)*higher_rate_tax
        additional_rate_tax_applied = (taxable_income - higher_rate_max)*additional_rate

        total_tax = basic_rate_tax_applied + higher_rate_tax_applied + additional_rate_tax_applied

    elif taxable_income>basic_rate_max:
        basic_rate_tax_applied = basic_rate_max*basic_rate_tax
        higher_rate_tax_applied = (taxable_income - basic_rate_max)*higher_rate_tax

        total_tax = basic_rate_tax_applied + higher_rate_tax_applied

    else:
        basic_rate_tax_applied = taxable_income*basic_rate_tax
        total_tax = basic_rate_tax_applied

    return TaxedIncomeUKTax(
        total_income=total_income,
        basic_tax=basic_rate_tax_applied,
        higher_tax=higher_rate_tax_applied,
        additional_tax=additional_rate_tax_applied,
        personal_allowance_reduction=personal_allowance_reduction)


# 9569 - 50270 tax 9%  # class 4 basic 9%
# 50270 - inf tax 2%   # class 4 basic 2%
def uk_class_4_tax(
    self_employment_net_income: int|float = 0,
    other_income: int|float = 0,
    basic_rate_min: int|float = 9569,
    basic_rate_max: int|float = 50270,
    basic_rate_tax_percentage: int|float = 9,
    higher_rate_tax_percentage: int|float = 2,
):
    basic_rate_tax_percentage = basic_rate_tax_percentage/100
    higher_rate_tax_percentage = higher_rate_tax_percentage/100

    total_selfemployment_income = self_employment_net_income + other_income
    
    class_4_basic_rate = 0
    class_4_higher_rate = 0
    total_tax = 0
    if basic_rate_min<=total_selfemployment_income<=basic_rate_max:
        class_4_basic_rate = (total_selfemployment_income-basic_rate_min) * basic_rate_tax_percentage
    elif total_selfemployment_income>basic_rate_max:
        class_4_basic_rate = (basic_rate_max-basic_rate_min) * basic_rate_tax_percentage
        class_4_higher_rate = (total_selfemployment_income-basic_rate_max) * higher_rate_tax_percentage

    total_tax = class_4_higher_rate + class_4_basic_rate

    return TaxedIncomeUKClass4(
        self_employment_net_income = self_employment_net_income,
        other_income = other_income,
        class_4_higher_rate_tax = class_4_higher_rate,
        class_4_basic_rate_tax = class_4_basic_rate
    )


def uk_class_2_tax(
    self_employment_net_income: int|float = 0,
    other_income: int|float = 0,
    tax_applied_for_income_above: int|float = 6475,
    flat_tax_amount: int|float = 159
):
    total_income = self_employment_net_income + other_income
    if total_income>tax_applied_for_income_above:
        return TaxedIncomeUKClass2(
            self_employment_net_income = self_employment_net_income,
            other_income = other_income,
            tax_applied = flat_tax_amount
        )
    return TaxedIncomeUKClass2(
        self_employment_net_income = self_employment_net_income,
        other_income = other_income,
        tax_applied = 0
    )



incomes = [20000] # [-10000, 0, 6470, 10000, 13000, 20000, 30000, 50000, 56000, 75000, 110000, 140000, 200000]
for income in incomes:
    uk = uk_tax(income)
    class_2 = uk_class_2_tax(income)
    class_4 = uk_class_4_tax(income)
    print(class_2)
    print(class_4)
    print(uk)
    print("===============================================================")
    print("Total Tax", class_2.total_tax+class_4.total_tax+uk.total_tax)
    print()
    print()
