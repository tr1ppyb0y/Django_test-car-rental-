from rest_framework import serializers
from .models import Vehicles
from user import serializers as user_serializers


class ListCreateVehicleSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False)
    class Meta:
        model = Vehicles
        fields = '__all__'

class UpdateDeleteVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'

