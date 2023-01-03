from rest_framework import serializers
from . import models as user_models

class SignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = user_models.User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True)
