from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from companies.models import SelfassesmentAccountSubmission, SelfassesmentAccountSubmissionTaxYear


class SelfemploymentIncomeSources(models.Model):
    class Meta:
        verbose_name = "Income Source"
        verbose_name_plural = "Income Sources"

    name = models.CharField(_("Name"), max_length=255)

    def __str__(self)->str:
        return self.name


class SelfemploymentExpenseSources(models.Model):
    class Meta:
        verbose_name = "Expense Source"
        verbose_name_plural = "Expense Sources"
    
    name = models.CharField(_("Name"), max_length=255)
    default_personal_usage_percentage = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self)->str:
        return self.name


class SelfemploymentDeductionSources(models.Model):
    class Meta:
        verbose_name = "Deduction Source"
        verbose_name_plural = "Deduction Sources"
    
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self)->str:
        return self.name


class Months(models.Model):
    class Meta:
        verbose_name = "Month"
        verbose_name_plural = "Months"
        ordering = ['month_index']
    
    month_name = models.CharField(_("Name"), max_length=10)
    month_index = models.IntegerField(_("Index"), default=0)

    def __str__(self)->str:
        return self.month_name


class SelfemploymentIncomesPerTaxYear(models.Model):
    class Meta:
        verbose_name = "Income Per Tax Year"
        verbose_name_plural = "Incomes Per Tax Year"
        constraints = [
            models.UniqueConstraint(fields=['client', 'month', 'income_source'], name="unique record")
        ]

    income_source = models.ForeignKey(SelfemploymentIncomeSources, on_delete=models.RESTRICT)
    client = models.ForeignKey(SelfassesmentAccountSubmission, on_delete=models.CASCADE)
    month = models.ForeignKey(Months, on_delete=models.RESTRICT)
    amount = models.FloatField(default=0)
    comission = models.FloatField(default=0)
    note = models.TextField(default='')

    def __str__(self) -> str:
        return f"{self.client.client_id.client_name} - {self.income_source} - {self.month} - {self.amount}"


class SelfemploymentExpensesPerTaxYear(models.Model):
    class Meta:
        verbose_name = "Expense Per Tax Year"
        verbose_name_plural = "Expenses Per Tax Year"
        constraints = [
            models.UniqueConstraint(fields=['client', 'month', 'expense_source'], name="unique expense record")
        ]

    expense_source = models.ForeignKey(SelfemploymentExpenseSources, on_delete=models.RESTRICT)
    client = models.ForeignKey(SelfassesmentAccountSubmission, on_delete=models.CASCADE)
    month = models.ForeignKey(Months, on_delete=models.RESTRICT)
    amount = models.FloatField(default=0)
    personal_usage_percentage = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    note = models.TextField(default='')

    def __str__(self) -> str:
        return f"{self.client.client_id.client_name} - {self.expense_source} - {self.month} - {self.amount}"


class SelfemploymentDeductionsPerTaxYear(models.Model):
    class Meta:
        verbose_name = "Deductions Per Tax Year"
        verbose_name_plural = "Deductions Per Tax Year"
        constraints = [
            models.UniqueConstraint(fields=['client', 'deduction_source'], name="unique deduction record")
        ]

    deduction_source = models.ForeignKey(SelfemploymentDeductionSources, on_delete=models.RESTRICT)
    client = models.ForeignKey(SelfassesmentAccountSubmission, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    allowance_percentage = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    personal_usage_percentage = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    note = models.TextField(default='')

    def __str__(self) -> str:
        return f"{self.client} - {self.deduction_source} - {self.amount}"

# class EmploymentIncomeForTaxYear(models.Model):
#     class Meta:
#         verbose_name = "Employment Income For Tax Year"
#         verbose_name_plural = "Employment Incomes For Tax Years"
    
#     submission = models.ForeignKey(SelfassesmentAccountSubmission, on_delete=models.RESTRICT)
#     income_amount = models.FloatField(default=0)
#     paid_tax_amount = models.FloatField(default=0)

#     def __str__(self) -> str:
#         return f"{self.submission} -  {self.income_amount} - {self.paid_tax_amount}"

class TaxableIncomeSources(models.Model):
    class Meta:
        verbose_name = "Taxable Income Source"
        verbose_name_plural = "Taxable Income Sources"
    name = models.CharField(default="New Taxable Income Source", max_length=255)
    apply_uk_tax = models.BooleanField()
    apply_class2_tax = models.BooleanField()
    apply_class4_tax = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.name} - uk tax {self.apply_uk_tax} - class 2 {self.apply_class2_tax} - class 4 tax {self.apply_class4_tax}"

class TaxableIncomeSourceForSubmission(models.Model):
    class Meta:
        verbose_name = "Taxable Income Source For Submission"
        verbose_name_plural = "Taxable Income Sources For Submissions"
    
    submission = models.ForeignKey(SelfassesmentAccountSubmission, on_delete=models.RESTRICT)
    taxable_income_source = models.ForeignKey(TaxableIncomeSources, on_delete=models.RESTRICT)
    income_amount = models.FloatField(default=0)
    paid_income_tax_amount = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"{self.submission} - income: {self.income_amount} - paid tax: {self.paid_income_tax_amount} - income source: {self.taxable_income_source.name}"

class SelfemploymentUkTaxConfigForTaxYear(models.Model):
    class Meta:
        verbose_name = 'Selfemployment UK Tax Config For TaxYear'
        verbose_name_plural = 'Selfemployment UK Tax Configs For TaxYears'
        constraints = [UniqueConstraint(name='unique_tax_year__uk_tax', fields=['tax_year'])]
    
    tax_year = models.ForeignKey(SelfassesmentAccountSubmissionTaxYear, on_delete=models.RESTRICT)
    # Allowance reduction configs
    personal_allowance_limit = models.FloatField(default=100000, blank=False, null=True)
    one_pound_reduction_from_PA_earned_over_PAL = models.FloatField(default=2, blank=False, null=True)
    
    # Tax brackets
    personal_allowance = models.FloatField(default=12570, blank=False, null=False)
    basic_rate_max = models.FloatField(default=37700, blank=False, null=False)
    higher_rate_max = models.FloatField(default=150000, blank=False, null=False)
    
    # Applied tax on each brackets
    basic_rate_tax_percentage = models.FloatField(default=20, blank=False, null=True)
    higher_rate_tax_percentage = models.FloatField(default=40, blank=False, null=True)
    additional_rate_tax_percentage = models.FloatField(default=45, blank=False, null=True)

    def __str__(self) -> str:
        return f"{self.tax_year} - {self.personal_allowance}, {self.basic_rate_max}, {self.higher_rate_max}"


class SelfemploymentClass4TaxConfigForTaxYear(models.Model):
    class Meta:
        verbose_name = 'Selfemployment Class 4 Tax Config For TaxYear'
        verbose_name_plural = 'Selfemployment Class 4 Tax Configs For TaxYears'
        constraints = [UniqueConstraint(name='unique_tax_year__class_4_tax', fields=['tax_year'])]
    
    tax_year = models.ForeignKey(SelfassesmentAccountSubmissionTaxYear, on_delete=models.RESTRICT)
    basic_rate_min = models.FloatField(default=9500, blank=False)
    basic_rate_max = models.FloatField(default=50000, blank=False)
    basic_rate_tax_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    higher_rate_tax_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self) -> str:
        return f"{self.tax_year} - {self.tax_applied_for_income_above} - {self.flat_tax_amount}"


class SelfemploymentClass2TaxConfigForTaxYear(models.Model):
    class Meta:
        verbose_name = 'Selfemployment Class 2 Tax Config For TaxYear'
        verbose_name_plural = 'Selfemployment Class 2 Tax Configs For TaxYears'
        constraints = [UniqueConstraint(name='unique_tax_year__class2_tax', fields=['tax_year'])]
    
    tax_year = models.ForeignKey(SelfassesmentAccountSubmissionTaxYear, on_delete=models.RESTRICT)
    tax_applied_for_income_above = models.FloatField(default=6470, blank=False)
    flat_tax_amount = models.FloatField(default=158, blank=False)

    def __str__(self) -> str:
        return f"{self.tax_year} - {self.tax_applied_for_income_above} - {self.flat_tax_amount}"
