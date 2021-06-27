from django.db.models import fields
from rest_framework import serializers
from users.models import CustomUser
from .models import Selfassesment, SelfassesmentAccountSubmission, SelfassesmentTracker
from .models import Limited


class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = '__all__'
    # fields = ['user_id', 'email', 'first_name', 'last_name', '']

class SelfassesmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Selfassesment
    # fields = '__all__'
    exclude = ['created_by']

class LimitedSerializer(serializers.ModelSerializer):
  class Meta:
    model = Limited
    # fields = '__all__'
    exclude = ['created_by']
