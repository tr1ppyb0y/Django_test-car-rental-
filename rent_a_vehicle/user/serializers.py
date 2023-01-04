from rest_framework import serializers
from . import models as user_models

class SignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = user_models.User
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = user_models.User
        fields = ['username', 'user_type', 'email', 'first_name', 'last_name', 'last_login']

class LoginLogsSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = user_models.UserLoginLogs
        fields = '__all__'