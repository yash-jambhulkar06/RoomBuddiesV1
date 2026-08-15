from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            "title",
            "description",
            "rent",
            "location",
            "room_type",
            "gender_preference",
            "is_available",
            "image",
        ]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Room Title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Describe your room...",
            }),
            "rent": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Monthly Rent",
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Location",
            }),
            "room_type": forms.Select(attrs={
                "class": "form-select",
            }),
            "gender_preference": forms.Select(attrs={
                "class": "form-select",
            }),
            "is_available": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control",
            }),
        }