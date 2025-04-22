from django import forms

from .models import Reservation, Dish, BookingReview


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guests', 'date', 'time', 'dishes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image']



class BookingReviewForm(forms.ModelForm):
    class Meta:
        model = BookingReview
        fields = ['rating', 'text']

    rating = forms.IntegerField(min_value=1, max_value=5, label='Оценка (1-5)')