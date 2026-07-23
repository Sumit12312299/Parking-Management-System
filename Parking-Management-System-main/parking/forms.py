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

    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data.get('vehicle_number', '').strip().upper()
        if not vehicle_number:
            raise forms.ValidationError("Vehicle number cannot be empty.")
        return vehicle_number