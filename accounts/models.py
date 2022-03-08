from email.policy import default
from django.db import models
from django.utils.translation import ugettext_lazy as _

from companies.models import SelfassesmentAccountSubmissionTaxYear, Selfassesment


class IncomeSources(models.Model):
    class Meta:
        verbose_name = "Income Source"
        verbose_name_plural = "Income Sources"

    name = models.CharField(_("Name"), max_length=255)

    def __str__(self)->str:
        return self.name


class ExpenseSources(models.Model):
    class Meta:
        verbose_name = "Expense Source"
        verbose_name_plural = "Expense Sources"
    
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


class IncomesPerTaxYear(models.Model):
    class Meta:
        verbose_name = "Income Per Tax Year"
        verbose_name_plural = "Incomes Per Tax Year"

    income_source = models.ForeignKey(IncomeSources, on_delete=models.RESTRICT)
    client = models.ForeignKey(Selfassesment, on_delete=models.RESTRICT)
    tax_year = models.ForeignKey(SelfassesmentAccountSubmissionTaxYear, on_delete=models.RESTRICT)
    month = models.ForeignKey(Months, on_delete=models.RESTRICT)
    amount = models.IntegerField(default=0)
    comission = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.client} - {self.income_source} - {self.tax_year} - {self.month} - {self.amount}"


class ExpensesPerTaxYear(models.Model):
    class Meta:
        verbose_name = "Expense Per Tax Year"
        verbose_name_plural = "Expenses Per Tax Year"

    expense_source = models.ForeignKey(IncomeSources, on_delete=models.RESTRICT)
    client = models.ForeignKey(Selfassesment, on_delete=models.RESTRICT)
    tax_year = models.ForeignKey(SelfassesmentAccountSubmissionTaxYear, on_delete=models.RESTRICT)
    month = models.ForeignKey(Months, on_delete=models.RESTRICT)
    amount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.client} - {self.expense_source} - {self.tax_year} - {self.month} - {self.amount}"
