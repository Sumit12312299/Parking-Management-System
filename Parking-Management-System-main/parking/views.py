from django.shortcuts import render

# Create your views here.
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Location, ParkingSlot

@login_required
def dashboard(request):
    locations = Location.objects.all()

    for location in locations:
        location.available_slots = ParkingSlot.objects.filter(
            location=location,
            is_available=True
        ).count()

    return render(request, 'parking/dashboard.html', {
        'locations': locations
    })

@login_required
def view_slots(request, location_id):
    location = Location.objects.get(id=location_id)
    slots = ParkingSlot.objects.filter(location=location)

    return render(request, 'parking/slots.html', {
        'location': location,
        'slots': slots
    })

from django.utils import timezone

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('slot', 'slot__location').order_by('-created_at')

    return render(request, 'parking/booking_history.html', {
        'bookings': bookings
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import ParkingSlot, Booking
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import ParkingSlot, Booking, Location
from .forms import BookingForm
from django.shortcuts import render
from datetime import datetime


@login_required
def book_slot(request, slot_id):
    slot = ParkingSlot.objects.get(id=slot_id)

    if not slot.is_available:
        messages.error(request, "Slot not available!")
        return redirect('location_slots', location_id=slot.location.id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():

            booking = form.save(commit=False)
            booking.user = request.user
            booking.slot = slot

            
            start = datetime.combine(booking.booking_date, booking.start_time)
            end = datetime.combine(booking.booking_date, booking.end_time)

            total_hours = (end - start).total_seconds() / 3600

            if total_hours <= 0:
                messages.error(request, "Invalid time selection!")
                return redirect('book_slot', slot_id=slot.id)

            booking.total_hours = round(total_hours,2)
            booking.total_amount = round(total_hours * 20,2)  

            booking.status = 'PENDING'
            booking.save()

            return redirect('payment_page', booking_id=booking.id)

    else:
        form = BookingForm()

    return render(request, 'parking/book_slot.html', {
        'form': form,
        'slot': slot
    })


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status='ACTIVE'
    )

    booking.status = 'CANCELLED'
    booking.save()

    slot = booking.slot
    slot.is_available = True
    slot.save()

    # Refund Calculation
    total_amount = booking.total_amount
    cancellation_fee = total_amount * 0.10 # 10% cancellation charge
    if cancellation_fee < 5 and total_amount > 5:
        cancellation_fee = 5
    elif cancellation_fee > total_amount:
        cancellation_fee = total_amount
    
    refund_amount = total_amount - cancellation_fee

    messages.success(request, f"Booking cancelled! ₹{cancellation_fee:.2f} cancellation fee applied. A refund of ₹{refund_amount:.2f} has been initiated to your account.")

    return redirect('booking_history')

from datetime import timedelta
@login_required
def extend_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='ACTIVE')
    
    if request.method == 'POST':
        hours_to_add = int(request.POST.get('hours', 1))
        
        # Add hours to end_time
        dt = datetime.combine(booking.booking_date, booking.end_time)
        dt = dt + timedelta(hours=hours_to_add)
        booking.end_time = dt.time()
        
        # Update cost and hours
        booking.total_hours += hours_to_add
        extra_charge = hours_to_add * 20
        booking.total_amount += extra_charge 
        booking.save()
        
        messages.success(request, f"Time Extended by {hours_to_add} hour(s)! ₹{extra_charge} extra charge added. Your new time is updated.")
        
    return redirect('booking_history')

def verify_ticket(request, booking_id):
    # This view is public so security guards can scan the QR code without logging in.
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'parking/verify_ticket.html', {'booking': booking})

@login_required
def payment_page(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":
        booking.status = "ACTIVE"
        booking.slot.is_available = False
        booking.slot.save()
        booking.save()

        messages.success(request, "Payment Successful & Slot Booked!")
        return redirect('booking_history')

    return render(request, 'parking/payment.html', {
        'booking': booking
    })

from django.shortcuts import render
from .models import Location

def explore_locations(request):
    city = request.GET.get('city')
    area = request.GET.get('area')

    locations = Location.objects.all()

    if city:
        locations = locations.filter(city=city)

    if area:
        locations = locations.filter(area=area)

    
    cities = Location.objects.values_list('city', flat=True).distinct()

    
    if city:
        areas = Location.objects.filter(city=city).values_list('area', flat=True).distinct()
    else:
        areas = Location.objects.values_list('area', flat=True).distinct()

    context = {
        'locations': locations,
        'cities': cities,
        'areas': areas,
        'selected_city': city,
        'selected_area': area,
    }

    return render(request, 'explore.html', context)