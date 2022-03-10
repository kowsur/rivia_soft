from django.db.models import fields
from rest_framework import serializers
from users.models import CustomUser
from .models import Selfassesment, SelfassesmentAccountSubmission, SelfassesmentAccountSubmissionTaxYear, SelfassesmentTracker
from .models import Limited


class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['user_id', 'email', 'first_name', 'last_name']

class SelfassesmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Selfassesment
    # fields = '__all__'
    exclude = ['created_by']

class SelfassesmentAccountSubmissionTaxYearSerializer(serializers.ModelSerializer):
  class Meta:
    model = SelfassesmentAccountSubmissionTaxYear
    fields = '__all__'


class SelfassesmentAccountSubmissionSerializer(serializers.ModelSerializer):
  client_id = SelfassesmentSerializer()
  tax_year = SelfassesmentAccountSubmissionTaxYearSerializer()
  submitted_by = CustomUserSerializer()
  prepared_by = CustomUserSerializer()
  last_updated_by = CustomUserSerializer()

  class Meta:
    model = SelfassesmentAccountSubmission
    fields = '__all__'


class LimitedSerializer(serializers.ModelSerializer):
  class Meta:
    model = Limited
    # fields = '__all__'
    exclude = ['created_by']
