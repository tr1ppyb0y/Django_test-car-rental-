import datetime
import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.db import models
from django.utils import timezone
from user.models import User


def car_image(instance, filename):
    return os.path.join('images/car/', datetime.datetime.now().date().strftime("%Y/%m/%d"), filename)


FULE_TYPE = (
    ('petrol', 'petrol'),
    ('diesel', 'diesel'),
    ('gasoline', 'gasoline'),
    ('battery', 'battery'),
)

CITIES = (
    ('jabalpur', 'Jabalpur'),
)

STATES = (
    ('madhya pradesh', 'Madhya Pradesh'),
)


class Vehicles(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=250, blank=False, null=False)
    color = models.CharField(max_length=100, blank=True, null=True)
    fuel_type = models.CharField(max_length=20, choices=FULE_TYPE, default='diesel')
    car_image = models.ImageField(upload_to=car_image, null=True, blank=True)
    price_per_hour = models.FloatField(default=1.0)
    is_avaliable = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    state = models.CharField(max_length=100, choices=STATES, default='Madhya Pradesh')
    city = models.CharField(max_length=100, choices=CITIES, default='Jabalpur')
    license_number = models.CharField(max_length=10, blank=False, null=False, unique=True)

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now(tz=timezone.utc)
        return super().save(*args, **kwargs)


REQUEST_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('completed', 'Completed')
)


class RentedLogs(models.Model):
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renter')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    requested_at = models.DateTimeField()
    rent_start = models.DateTimeField()
    rent_end = models.DateTimeField()
    fine = models.FloatField(default=0.0)
    pick_up_location = models.CharField(max_length=100)
    drop_location = models.CharField(max_length=100)
    request_status = models.CharField(max_length=50, choices=REQUEST_STATUS, default='pending')
    estimated_amount = models.FloatField(default=0.0)
    total_amount = models.CharField(max_length=100)
    fine = models.FloatField(default=10.0)

    def save(self, *args, **kwargs):
        channel_layers = get_channel_layer()
        if self._state.adding:
            self.estimated_amount = (self.rent_end-self.rent_end).seconds/(60*60) * self.vehicle.price_per_hour
            self.requested_at = datetime.datetime.now(tz=timezone.utc)
            logs_count = RentedLogs.objects.filter(request_status='pending').count()
            data = {'logs_count': logs_count, 'current_log': serializers.serialize('json', [self])}
            user_group_name = f'notification_{self.owner.id}'
            async_to_sync(channel_layers.group_send)(
                user_group_name, {
                    'type': 'send_owner_notification',
                    'value': data
                }
            )
        else:
            user_group_name = f'notification_{self.renter.id}'
            message = f'Your request for vehicle {self.vehicle.license_number} is {self.request_status}.'
            async_to_sync(channel_layers.group_send)(
                user_group_name, {
                    'type': 'send_renter_notification',
                    'value': message
                }
            )
        super(RentedLogs, self).save(*args, **kwargs)

    def get_total_amount(self):
        return (self.fine * (timezone.now() - self.rent_end).seconds/(60*60)) + self.estimated_amount
