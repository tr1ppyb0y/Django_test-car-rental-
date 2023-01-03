from django.urls import path
from . import views

urlpatterns = [
    path('list-add-vehicle/', views.ListCreateVehicleView.as_view(), name='list-add-vehicle'),
    path('retrive-update-delete-vehicle/<int:id>', views.RetrieveUpdateVehicleView.as_view(), name='retreve-update-delete-vehicle'),
    path('vehicle-logs/', views.vehicle_logs, name='vehicle-logs'),
]