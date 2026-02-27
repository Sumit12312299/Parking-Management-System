from django.db import models

# Create your models here.
from django.conf import settings
from django.utils import timezone

class Location(models.Model):
    LOCATION_TYPES = [
        ('Mall', 'Mall'),
        ('Hotel', 'Hotel'),
        ('College', 'College'),
        ('Office', 'Office'),
        ('Restaurant', 'Restaurant'),
    ]

    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPES)

    def __str__(self):
        return f"{self.name} - {self.area}, {self.city}"


class ParkingSlot(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    slot_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.location.name} - {self.slot_number}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slot = models.ForeignKey('ParkingSlot', on_delete=models.CASCADE)

    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    total_hours = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.slot.slot_number}"




