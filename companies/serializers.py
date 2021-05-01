from django.db.models import fields
from rest_framework import serializers
from .models import Selfassesment, SelfassesmentAccountSubmission, SelfassesmentTracker
from users.models import CustomUser


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
