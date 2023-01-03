from . import serializers as vehicle_serializers
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import Vehicles, RentedLogs
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
# Create your views here.

class ListCreateVehicleView(generics.ListCreateAPIView):
    queryset = Vehicles.objects.filter(is_avaliable=True)
    permission_classes = permissions.IsAuthenticated
    serializer_class = vehicle_serializers.ListCreateVehicleSerializer

class RetrieveUpdateVehicleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicles.objects.all()
    permission_classes = permissions.IsAuthenticated
    serializer_class = vehicle_serializers.ListCreateVehicleSerializer
    lookup_field = 'id'

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, ])
def vehicle_logs(request):
    if request.user.user_type == 'owner':
        queryset = RentedLogs.objects.filter(owner=request.user)
    else:
        queryset = RentedLogs.objects.filter(renter=request.user)
    serializer = vehicle_serializers.ListCreateVehicleSerializer(data=queryset, many=True)
    content = {'data':serializer.data, 'message':'Vehicles borrowed from you.'}
    return JsonResponse(content)