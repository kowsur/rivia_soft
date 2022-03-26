from rest_framework import serializers

from companies.serializers import SelfassesmentAccountSubmissionSerializer
from .models import SelfemploymentIncomeSources, SelfemploymentExpenseSources, Months, SelfemploymentIncomesPerTaxYear, SelfemploymentExpensesPerTaxYear


class SelfemploymentIncomeSourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfemploymentIncomeSources
        fields = '__all__'


class SelfemploymentExpenseSourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelfemploymentExpenseSources
        fields = '__all__'


class MonthsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Months
        fields = '__all__'


class SelfemploymentIncomesPerTaxYearSerializer(serializers.ModelSerializer):
    # income_source = IncomeSourcesSerializer()
    # client = SelfassesmentAccountSubmissionSerializer()
    # month = MonthsSerializer()

    class Meta:
        model = SelfemploymentIncomesPerTaxYear
        fields = '__all__'


class SelfemploymentExpensesPerTaxYearSerializer(serializers.ModelSerializer):
    # expense_source = ExpenseSourcesSerializer()
    # client = SelfassesmentAccountSubmissionSerializer()
    # month = MonthsSerializer()

    class Meta:
        model = SelfemploymentExpensesPerTaxYear
        fields = '__all__'

