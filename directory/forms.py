from django import forms
from .models import Offer, Request


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'skill', 'title', 'description', 'hour_value', 'availability', 'location', 'is_active'
        ]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'skill', 'title', 'description', 'hours_needed', 'when', 'location', 'is_active'
        ]


