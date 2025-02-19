from django import forms
from .models import Session

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date', 'session_type']
        widgets = {
            'date': forms.DateInput(
                format =('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }