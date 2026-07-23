from django.db import models
from django.conf import settings
from django.utils import timezone


class Location(models.Model):
    """
    Represents a physical parking location (e.g. Mall, Hotel, Office).
    """
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

    def __str__(self) -> str:
        return f"{self.name} - {self.area}, {self.city}"


class ParkingSlot(models.Model):
    """
    Represents an individual parking slot within a specific location.
    """
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='slots')
    slot_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.location.name} - {self.slot_number}"


class Booking(models.Model):
    """
    Represents a user reservation for a specific parking slot.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE, related_name='bookings')

    vehicle_number = models.CharField(max_length=20, default="NOT-PROVIDED")

    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    total_hours = models.FloatField(default=0)
    total_amount = models.FloatField(default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self) -> bool:
        """Returns True if the booking status is active."""
        return self.status == 'ACTIVE'

    def __str__(self) -> str:
        return f"{self.user.username} - {self.slot.slot_number} ({self.vehicle_number})"
