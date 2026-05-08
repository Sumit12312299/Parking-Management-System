from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['vehicle_number', 'booking_date', 'start_time', 'end_time']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={'placeholder': 'e.g. DL-04-AB-1234', 'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }