from django.shortcuts import render

# Create your views here.
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Location, ParkingSlot

def dashboard(request):
    locations = Location.objects.all()

    for location in locations:
        location.available_slots = ParkingSlot.objects.filter(
            location=location,
            is_available=True
        ).count()

    active_bookings = []
    if request.user.is_authenticated:
        from .models import Booking
        active_bookings = Booking.objects.filter(
            user=request.user,
            status='ACTIVE'
        ).select_related('slot', 'slot__location').order_by('-created_at')

    return render(request, 'parking/dashboard.html', {
        'locations': locations,
        'active_bookings': active_bookings
    })



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

    for location in locations:
        location.available_slots = ParkingSlot.objects.filter(
            location=location,
            is_available=True
        ).count()

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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import urllib.request
from django.conf import settings

@csrf_exempt
def chatbot_api(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required"}, status=400)
    
    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").strip()
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    if not user_message:
        return JsonResponse({"reply": "Type something to chat!"})
        
    # Compile real-time database context
    try:
        locations = Location.objects.all()
        locations_list = []
        for loc in locations:
            total = ParkingSlot.objects.filter(location=loc).count()
            avail = ParkingSlot.objects.filter(location=loc, is_available=True).count()
            slots_list = list(ParkingSlot.objects.filter(location=loc).values_list('slot_number', flat=True))
            locations_list.append(
                f"- {loc.name} (Type: {loc.location_type}, Area: {loc.area}, City: {loc.city}): "
                f"Total slots = {total}, Available slots = {avail}, Booked slots = {total - avail}. "
                f"Slot numbers are: {', '.join(slots_list)}."
            )
        locations_context = "\n".join(locations_list)
    except Exception as e:
        locations_context = "Locations are standard malls, hotels, and offices."

    pricing_context = (
        "Our standard parking fee is ₹20 per hour. The price is calculated as ₹20 * hours. For example, 3 hours costs ₹60. "
        "Refund Policy: Yes, bookings are fully refundable! If a user cancels their active booking from their 'My Bookings' page, "
        "a standard 10% cancellation fee is applied, and the remaining 90% of the total amount is refunded instantly to their account."
    )
    
    system_prompt = (
        "You are ParkBot, the official smart AI assistant for ParkKaro, a premium Parking Management System. "
        "Answer the user's questions politely, professionally, and naturally. "
        "Always use the following real-time database context to answer accurately:\n\n"
        "=== REAL-TIME PARKING LOCATIONS DATA ===\n"
        f"{locations_context}\n\n"
        "=== PRICING DATA ===\n"
        f"{pricing_context}\n\n"
        "=== SYSTEM INSTRUCTIONS ===\n"
        "1. Give direct, clear, and helpful answers.\n"
        "2. Keep replies concise and easy to read.\n"
        "3. Use bold text and emojis to make replies attractive.\n"
        "4. If a user says 'do a booking for me' or asks to book a slot, tell them you CAN do this for them. Ask them for any missing details:\n"
        "   - Location Name\n"
        "   - Slot Number (must be an available slot number for that location from the data above)\n"
        "   - Vehicle Number\n"
        "   - Date (format: YYYY-MM-DD)\n"
        "   - Start Time (format: HH:MM, e.g., 14:00)\n"
        "   - End Time (format: HH:MM, e.g., 16:00)\n"
        "5. Once you have ALL details from the user, confirm the booking and YOU MUST append a special action block at the very end of your response exactly like this (with NO extra characters inside the brackets):\n"
        "   [BOOK_ACTION] {\"location_name\": \"...\", \"slot_number\": \"...\", \"vehicle_number\": \"...\", \"date\": \"...\", \"start_time\": \"...\", \"end_time\": \"...\"}\n"
        "6. Speak in English or Hinglish depending on how the user asks."
    )
    
    # Call Gemini API safely using urllib
    api_key = getattr(settings, "GEMINI_API_KEY", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt},
                    {"text": f"User: {user_message}"}
                ]
            }
        ]
    }
    
    try:
        req_data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            reply = res_data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        # Smart rule-based fallback when Gemini API key fails or is rate-limited/leaked
        msg_lower = user_message.lower()
        if any(kw in msg_lower for kw in ["charge", "pricing", "price", "cost", "fee", "rate", "money", "rupee", "pay"]):
            reply = (
                "💰 **Parking Charges & Pricing:**\n\n"
                f"{pricing_context}\n\n"
                "To book a slot, go to your **Dashboard**, select a location, and select any available slot! 😊"
            )
        elif any(kw in msg_lower for kw in ["refund", "cancel", "policy"]):
            reply = (
                "🔄 **Refund & Cancellation Policy:**\n\n"
                "Yes, bookings are **fully refundable**! "
                "If you cancel an active booking from your 'My Bookings' page, a standard **10% cancellation fee** is applied, "
                "and the remaining **90% is refunded instantly** to your account. 😊"
            )
        elif any(kw in msg_lower for kw in ["location", "avail", "slot", "where", "place", "mall", "hotel", "college", "office", "restaurant"]):
            reply = (
                "📍 **Real-time Parking Locations & Slot Availability:**\n\n"
                f"{locations_context}\n\n"
                "Click **Browse Locations** on the dashboard to see them on a map! 🚗"
            )
        elif any(kw in msg_lower for kw in ["book", "reserve", "how to"]):
            reply = (
                "🚗 **How to Book a Parking Slot:**\n\n"
                "1. Go to the **Dashboard**.\n"
                "2. Click **View Slots** or **Browse Locations** on your preferred venue.\n"
                "3. Select any available green slot from the interactive visual map.\n"
                "4. Enter your vehicle number, select the date, start time, and end time.\n"
                "5. Complete the secure payment to lock your spot instantly! 🔒\n\n"
                "Feel free to ask me any other questions! 😊"
            )
        elif any(kw in msg_lower for kw in ["hello", "hi", "hey", "greetings", "who are you", "bot"]):
            reply = (
                "👋 **Hello! I am ParkBot, your smart AI assistant for ParkKaro!**\n\n"
                "I can help you check charges, find real-time available locations/slots, "
                "explain our refund policy, or guide you through booking. How can I assist you today? 😊"
            )
        elif any(kw in msg_lower for kw in ["support", "contact", "phone", "email", "help", "care"]):
            reply = (
                "📞 **Customer Support & Help:**\n\n"
                "Our premium customer support team is available 24/7!\n"
                "- 📧 **Email:** support@parkkaro.com\n"
                "- 📞 **Phone:** +91 98765 43210\n\n"
                "Feel free to reach out to us if you need any manual assistance! 😊"
            )
        else:
            reply = (
                "👋 **I am ParkBot, your smart assistant!**\n\n"
                "It looks like our AI is currently offline, but I can still assist you locally! "
                "You can ask me about:\n"
                "- 💰 **'Parking Charges'** or pricing\n"
                "- 🔄 **'Refund Policy'** or cancellations\n"
                "- 📍 **'Available Locations'** to see real-time slots\n"
                "- 🚗 **'How to Book'** for a quick guide\n\n"
                "How can I help you today? 😊"
            )

    # Smart Booking Automation Parsing
    if "[BOOK_ACTION]" in reply:
        try:
            parts = reply.split("[BOOK_ACTION]")
            text_reply = parts[0].strip()
            action_json_str = parts[1].strip()
            action_data = json.loads(action_json_str)
            
            if request.user.is_authenticated:
                loc_name = action_data.get("location_name")
                slot_num = action_data.get("slot_number")
                veh_num = action_data.get("vehicle_number", "NOT-PROVIDED")
                b_date_str = action_data.get("date")
                s_time_str = action_data.get("start_time")
                e_time_str = action_data.get("end_time")
                
                from datetime import datetime, date
                b_date = datetime.strptime(b_date_str, "%Y-%m-%d").date() if b_date_str else date.today()
                s_time = datetime.strptime(s_time_str, "%H:%M").time()
                e_time = datetime.strptime(e_time_str, "%H:%M").time()
                
                # Fetch slot
                slot = ParkingSlot.objects.filter(
                    location__name__icontains=loc_name,
                    slot_number=slot_num
                ).first()
                
                if slot:
                    if slot.is_available:
                        start = datetime.combine(b_date, s_time)
                        end = datetime.combine(b_date, e_time)
                        total_hours = (end - start).total_seconds() / 3600
                        
                        if total_hours > 0:
                            booking = Booking.objects.create(
                                user=request.user,
                                slot=slot,
                                vehicle_number=veh_num,
                                booking_date=b_date,
                                start_time=s_time,
                                end_time=e_time,
                                total_hours=round(total_hours, 2),
                                total_amount=round(total_hours * 20, 2),
                                status='PENDING'
                            )
                            reply = (
                                f"{text_reply}\n\n"
                                f"🎉 **Great news! I have successfully processed a pending booking for you!**\n"
                                f"📍 **Location:** {slot.location.name}\n"
                                f"🚗 **Slot Number:** {slot.slot_number}\n"
                                f"💰 **Total Cost:** ₹{booking.total_amount} ({booking.total_hours} hours)\n\n"
                                f"👉 [**Click here to complete your Payment**](/payment/{booking.id}/) to lock your spot!"
                            )
                        else:
                            reply = "Invalid booking times provided. Please make sure the end time is after the start time!"
                    else:
                        reply = f"Ah, slot {slot_num} at {loc_name} is already booked. Could you please select another slot? 😊"
                else:
                    reply = f"I couldn't find slot {slot_num} at {loc_name} in our system. Please check available slots and try again! 😊"
            else:
                reply = f"{text_reply}\n\n⚠️ Please [**Login**](/accounts/login/) first to perform automated bookings! 😊"
        except Exception as e:
            pass
        
    return JsonResponse({"reply": reply})