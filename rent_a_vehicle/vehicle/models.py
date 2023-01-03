from django.db import models
import os, datetime
from user.models import User
from django.utils import timezone

def car_image(instance, filename):
    return os.path.join('images/car/', datetime.datetime.now().date().strftime("%Y/%m/%d"), filename)

FULE_TYPE = (
    ('petrol', 'petrol'),
    ('diesel', 'diesel'),
    ('gasoline', 'gasoline'),
    ('battery', 'battery'),
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

    def save(self, *args, **kwargs):
        self.rented_at = datetime.datetime.now(tz=timezone.utc)
        return super().save(*args, **kwargs)

class RentedLogs(models.Model):
    vehicles = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renter')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    rented_at = models.DateTimeField()
    rented_duration = models.DateTimeField()
    fine = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        self.rented_at = datetime.datetime.now(tz=timezone.utc)
        return super().save(*args, **kwargs)
