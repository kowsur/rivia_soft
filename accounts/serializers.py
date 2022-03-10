from rest_framework import serializers

from companies.serializers import SelfassesmentAccountSubmissionSerializer
from .models import IncomeSources, ExpenseSources, Months, IncomesPerTaxYear, ExpensesPerTaxYear


class IncomeSourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeSources
        fields = '__all__'


class ExpenseSourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSources
        fields = '__all__'


class MonthsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Months
        fields = '__all__'


class IncomesPerTaxYearSerializer(serializers.ModelSerializer):
    income_source = IncomeSourcesSerializer()
    client = SelfassesmentAccountSubmissionSerializer()
    month = MonthsSerializer()

    class Meta:
        model = IncomesPerTaxYear
        fields = '__all__'


class ExpensesPerTaxYearSerializer(serializers.ModelSerializer):
    income_source = ExpenseSourcesSerializer()
    client = SelfassesmentAccountSubmissionSerializer()
    month = MonthsSerializer()

    class Meta:
        model = IncomesPerTaxYear
        fields = '__all__'

