# https://taxscouts.com/calculator/national-insurance/

from math import inf
from dataclasses import dataclass
from typing import List


@dataclass
class TaxPolicy:
    start: int|float
    end: int|float
    tax_percentage: int|float|None = None # this sould be between 0 and 100
    flat_tax: int|float|None = None


    def __post_init__(self):
        # Check for values
        if self.flat_tax is None and self.tax_percentage is None:
            raise ValueError(f"{self.__class__.__name__}.tax_percentage or {self.__class__.__name__}.flat_tax must be specified")
        
        # Don't allow flat_tax and tax_percentage at the same time
        if self.flat_tax is not None and self.tax_percentage is not None:
            raise ValueError(f"You should specify one of {self.__class__.__name__}.tax_percentage or {self.__class__.__name__}.flat_tax")

        if self.tax_percentage is not None and not 0<=self.tax_percentage<=100:
            raise ValueError(f"{self.__class__.__name__}.tax_percentage must be an int or a float and the value must be between 0 and 100")
        
        if self.flat_tax is not None and self.flat_tax<0:
            raise ValueError(f"{self.__class__.__name__}.flat_tax must be greter than or equals to 0")

        # set initial values
        if self.flat_tax is None:
            self.flat_tax = 0
        if self.tax_percentage is None:
            self.tax_percentage = 0

    def calc_tax(self, income) -> int|float:
        """This calc function should only be used if the TaxPolicy is not in any ProgressiveTaxPolicy.
        """
        total_tax = 0
        if self.start<=income<=self.end:
            total_tax += self.flat_tax
            total_tax += (income-self.start)*self.tax_percentage/100
        if income>self.end:
            total_tax += self.flat_tax
            total_tax += (self.end-self.start)*self.tax_percentage/100
        return total_tax


@dataclass
class ProgressiveTaxPolicy:
    policies: List[TaxPolicy]
    
    # for uk personal_allowance_limit is 100,000£ but for those who doesn't have any limit the personal_allowance_limit
    # could be passed as math.inf, the limit is applied if the polici
    personal_allowance_limit: int|float = 100000 # math.inf for no limit
    
    # when personal_allowance_limit exceeds 1£ is redued from personal_allowance per 2£ earned over personal_allowance_limit
    # PAL - Personal Allowance Limit
    one_unit_deducted_from_personal_allowance_earned_over_PAL: int|float = 2


    def __post_init__(self):
        self.policies = sorted(self.policies, key=lambda policy: (policy.tax_percentage, policy.start))
        
        if self.one_unit_deducted_from_personal_allowance_earned_over_PAL<=0:
            raise ValueError(f"{self.__class__.__name__}.one_unit_deducted_from_personal_allowance_earned_over_PAL must be greater than 0")
    

    @property
    def first_policy(self) -> TaxPolicy|None:
        return self.policies[0] if len(self.policies)>0 else None
    
    @property
    def personal_allowance(self) -> int|float|None:
        return self.first_policy.end if type(self.first_policy)==TaxPolicy else None
    
    @property
    def last_policy(self) -> TaxPolicy|None:
        return self.policies[-1] if len(self.policies)>0 else None
    
    @property
    def last_policy_start(self):
        return self.last_policy.start if type(self.first_policy)==TaxPolicy else None
    

    def calc_tax(self, income:int|float) -> int|float:
        """Calculates progressive tax on income using the specified tax brackets/Policies
        """
        income = income
        # As for every 2£ earned over 100,000£ 1£ is substracted from Personal allowance
        # Getting the amount that is subtracted from Personal Allowance
        personal_allowance_reduction = 0
        if (income>=self.personal_allowance_limit):
            personal_allowance_reduction = (income - self.personal_allowance_limit)/self.one_unit_deducted_from_personal_allowance_earned_over_PAL
            if (personal_allowance_reduction>self.personal_allowance):
                personal_allowance_reduction = self.personal_allowance
        
        total_tax = 0
        for policy_idx, policy in enumerate(self.policies):
            bracket_start = policy.start - personal_allowance_reduction
            bracket_end = policy.end - personal_allowance_reduction

            if policy_idx==len(self.policies)-2:
                bracket_end = self.last_policy_start

            if policy is self.last_policy:
                bracket_start = policy.start
                bracket_end = policy.end
            
            
            if income>bracket_start:
                additive_tax = policy.flat_tax
                
                # Calulate applicable tax for current tax TaxPolicy\bracket
                if income>=bracket_end:
                    additive_tax += (bracket_end-bracket_start) * policy.tax_percentage/100
                else:
                    taxable_income_for_bracket = income-bracket_start
                    if taxable_income_for_bracket<1:
                        continue
                    additive_tax += taxable_income_for_bracket*policy.tax_percentage/100
                
                total_tax+=additive_tax

        return total_tax



year_18_19 = [
            TaxPolicy(0, 11850, 0), # Personal Allowance
            TaxPolicy(11850, 46350, 20), # Basic Rate
            TaxPolicy(46350, 150000, 40), # Higher Rate
            TaxPolicy(150000, inf, 45), # Additional Rate
        ]
year_19_20 = [
            TaxPolicy(0, 12500, 0), # Personal Allowance
            TaxPolicy(12500, 50000, 20), # Basic Rate
            TaxPolicy(50000, 150000, 40), # Higher Rate
            TaxPolicy(150000, inf, 45), # Additional Rate
        ]
year_20_21 = [
        TaxPolicy(0, 12500, 0), # Personal Allowance
        TaxPolicy(12500, 50000, 20), # Basic Rate
        TaxPolicy(50000, 150000, 40), # Higher Rate
        TaxPolicy(150000, inf, 45), # Additional Rate
        ]
year_21_22 = [
            TaxPolicy(0, 12570, 0), # Personal Allowance
            TaxPolicy(12570, 50270, 20), # Basic Rate
            TaxPolicy(50270, 150000, 40), # Higher Rate
            TaxPolicy(150000, inf, 45), # Additional Rate
        ]
year_22_23 = [
            TaxPolicy(start=0, end=12570, tax_percentage=0), # Personal Allowance
            TaxPolicy(start=12570, end=50270, tax_percentage=20), # Basic Rate
            TaxPolicy(start=50270, end=150000, tax_percentage=40), # Higher Rate
            TaxPolicy(start=150000, end=inf, tax_percentage=45), # Additional Rate
        ]
year_21_22_eng = [
            TaxPolicy(start=0, end=37700, tax_percentage=20), # Basic Rate
            TaxPolicy(start=37700, end=150000, tax_percentage=40), # Higher Rate
            TaxPolicy(start=150000, end=inf, tax_percentage=45), # Additional Rate
        ]
class_4_policies = [
            TaxPolicy(start=9569, end=50270, tax_percentage=9), # 9% on profits between £9,569 and £50,270
            TaxPolicy(start=50270, end=inf, tax_percentage=2), # 2% on profits over £50,270
        ]

class_2 = TaxPolicy(6515, inf, flat_tax=158)
class_4 = ProgressiveTaxPolicy(policies=class_4_policies, personal_allowance_limit=inf)
uk_tax = ProgressiveTaxPolicy(policies=year_22_23, personal_allowance_limit=100000)



incomes = [-20000, 10000, 20000, 50000, 75000, 80000, 110000, 130000, 180000, 200000, 160000, 300000, 1600000]
for income in incomes:
    uk_tax_amount = uk_tax.calc_tax(income)
    class_2_amount = class_2.calc_tax(income)
    class_4_amount = class_4.calc_tax(income)
    total_tax = class_2_amount + class_4_amount + uk_tax_amount
    #  'class_2_tax',class_2_amount, 'class_4_tax', class_4_amount
    # 'total_tax', total_tax, 
    print('income', income, 'uk_tax', uk_tax_amount)
