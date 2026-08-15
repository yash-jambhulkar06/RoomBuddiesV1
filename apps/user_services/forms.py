from django import forms

from .models import ServiceBooking


class ServiceBookingForm(forms.ModelForm):

    class Meta:
        model = ServiceBooking

        fields = [
            "booking_type",
            "booking_date",
        ]

        widgets = {
            "booking_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "booking_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }