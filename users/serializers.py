from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('user_id', 'email', 'first_name', 'last_name')


# user = CustomUser.objects.get(pk=1)
# response = CustomUserSerializer(instance=user).data