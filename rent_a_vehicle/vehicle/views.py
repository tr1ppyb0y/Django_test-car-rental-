from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)

from . import serializers as vehicle_serializers
from .models import RentedLogs, Vehicles

# Create your views here.


class ListCreateVehicleView(generics.ListCreateAPIView):
    queryset = Vehicles.objects.filter(is_avaliable=True)
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = vehicle_serializers.ListCreateVehicleSerializer


class RetrieveUpdateVehicleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicles.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = vehicle_serializers.ListCreateVehicleSerializer
    lookup_field = 'id'


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([permissions.IsAuthenticated, ])
def vehicle_logs(request):
    if request.user.user_type == 'owner':
        queryset = RentedLogs.objects.filter(owner=request.user)
    else:
        queryset = RentedLogs.objects.filter(renter=request.user)
    serializer = vehicle_serializers.ListCreateVehicleSerializer(queryset, many=True)
    content = {'data':serializer.data, 'message':'Vehicles rent logs.'}
    return JsonResponse(content)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([permissions.IsAuthenticated, ])
def rent_a_vehicle(request, vehicle_id):
    serializer = vehicle_serializers.RentLogsSerializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        vehicle = Vehicles.objects.get(id=vehicle_id)
        rent_logs = serializer.validated_data
        rent_logs_dict = dict(rent_logs.items())
        RentedLogs.objects.create(
            vehicle=vehicle, renter=request.user.id, owner=vehicle.owner,
            **rent_logs_dict
        )
        return JsonResponse({'message': 'Your request has been sent to the owner of the vehicle. You will be receiving notification shortly.'})
    return JsonResponse({'message': serializer.errors})
