from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from .models import Location, ParkingSlot, Booking

User = get_user_model()

class ParkingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testdriver',
            email='testdriver@example.com',
            password='testpassword123'
        )
        self.location = Location.objects.create(
            city='Delhi',
            area='Connaught Place',
            name='CP Central Parking',
            location_type='Mall'
        )
        self.slot = ParkingSlot.objects.create(
            location=self.location,
            slot_number='A-101',
            is_available=True
        )

    def test_location_str(self):
        self.assertEqual(str(self.location), "CP Central Parking - Connaught Place, Delhi")

    def test_parking_slot_str(self):
        self.assertEqual(str(self.slot), "CP Central Parking - A-101")
        self.assertTrue(self.slot.is_available)

    def test_booking_creation_and_str(self):
        today = datetime.date.today()
        start = datetime.time(10, 0)
        end = datetime.time(12, 0)
        booking = Booking.objects.create(
            user=self.user,
            slot=self.slot,
            vehicle_number='DL-01-AB-1234',
            booking_date=today,
            start_time=start,
            end_time=end,
            total_hours=2.0,
            total_amount=100.0,
            status='ACTIVE'
        )
        self.assertEqual(str(booking), "testdriver - A-101 (DL-01-AB-1234)")
        self.assertEqual(booking.status, 'ACTIVE')
        self.assertEqual(booking.total_amount, 100.0)
