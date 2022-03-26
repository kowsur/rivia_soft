from django.contrib import admin

from .models import SelfemploymentIncomeSources, SelfemploymentExpenseSources, Months, SelfemploymentIncomesPerTaxYear, SelfemploymentExpensesPerTaxYear


admin.site.register([SelfemploymentIncomeSources, SelfemploymentExpenseSources, Months, SelfemploymentIncomesPerTaxYear, SelfemploymentExpensesPerTaxYear])
