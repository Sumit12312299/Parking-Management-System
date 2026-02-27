from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Location, ParkingSlot, Booking

admin.site.register(Location)
admin.site.register(ParkingSlot)
admin.site.register(Booking)