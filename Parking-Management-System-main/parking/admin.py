from django.contrib import admin
from .models import Location, ParkingSlot, Booking

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'area', 'location_type')
    list_filter = ('location_type', 'city')
    search_fields = ('name', 'city', 'area')
    ordering = ('city', 'name')

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'location', 'is_available')
    list_filter = ('is_available', 'location')
    search_fields = ('slot_number', 'location__name')
    ordering = ('location', 'slot_number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slot', 'vehicle_number', 'booking_date', 'start_time', 'end_time', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'booking_date')
    search_fields = ('vehicle_number', 'user__username', 'slot__slot_number', 'slot__location__name')
    ordering = ('-created_at',)