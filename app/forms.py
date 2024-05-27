from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = 'date'


class ExampleForm(forms.Form):
    my_date = forms.DateField(widget=DateInput)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=("Přihlašovací jméno"))
    password = forms.CharField(label=("Heslo"), widget=forms.PasswordInput)


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(label="Přihlašovací jméno")
    password1 = forms.CharField(label="Heslo", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Potvrďte Heslo", widget=forms.PasswordInput)

