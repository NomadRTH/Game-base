from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
    min_value=1,
    max_value=10,
    widget=forms.NumberInput(attrs={'class': 'rating-input'})
)
    class Meta:
        model = Review
        fields = ["feedback", "rating"]