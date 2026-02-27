from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Location, ParkingSlot


@receiver(post_save, sender=Location)
def create_parking_slots(sender, instance, created, **kwargs):
    if created:
        
        slot_count_map = {
            'MALL': 200,
            'HOTEL': 80,
            'COLLEGE': 150,
            'OFFICE': 100,
            'COMMERCIAL': 120,
        }

        total_slots = slot_count_map.get(instance.location_type, 50)

        for i in range(1, total_slots + 1):
            ParkingSlot.objects.create(
                location=instance,
                slot_number=f"S{i}",
                is_available=True
            )
            