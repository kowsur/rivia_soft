from django.contrib import admin

from .models import IncomeSources, ExpenseSources, Months, IncomesPerTaxYear, ExpensesPerTaxYear


admin.site.register([IncomeSources, ExpenseSources, Months])
