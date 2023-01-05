from django.urls import path

from . import views

urlpatterns = [
    path('list-add-vehicle/', views.ListCreateVehicleView.as_view(), name='list-add-vehicle'),
    path('retrive-update-delete-vehicle/<int:id>', views.RetrieveUpdateVehicleView.as_view(), name='retreve-update-delete-vehicle'),
    path('rent-a-vehicle/int:vehicle_id>', views.rent_a_vehicle, name='rent-a-vehicle'),
    path('vehicle-logs/', views.vehicle_logs, name='vehicle-logs'),
]
