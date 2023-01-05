from rest_framework import serializers

from .models import RentedLogs, Vehicles


class ListCreateVehicleSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Vehicles
        fields = '__all__'


class UpdateDeleteVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'


class RentLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentedLogs
        fields = ['vehicle', 'rent_start', 'rent_end', 'pick_up_location', 'drop_location']
