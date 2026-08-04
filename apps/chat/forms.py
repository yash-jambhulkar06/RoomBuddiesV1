from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=["message"]
        
        widgets={
            "message":forms.TextInput(
                attrs={
                    "id":"chat-message-input",
                    "class":"form-control",
                    "placeholder":"Type your message...",
                    "autocomplete":"off",
                }
            )
        }