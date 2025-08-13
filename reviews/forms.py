from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    comment = forms.CharField(max_length=140, required=False, widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'Optional comment (140 chars)'
    }))

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }

