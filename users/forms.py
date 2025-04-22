from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Reservation

from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Роль")

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'role']

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class LoginForm(AuthenticationForm):
    pass


class VerifyEmailForm(forms.Form):
    code = forms.CharField(max_length=6, label="Код подтверждения")


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests', 'dishes']
