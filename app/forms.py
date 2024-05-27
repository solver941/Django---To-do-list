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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Heslo"
        self.fields['password2'].label = "Potvrďte Heslo"

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(
                "Hesla se neshodují."
            )

        return cleaned_data

    def _post_clean(self):
        super()._post_clean()
        password2 = self.cleaned_data.get('password2')
        if password2:
            try:
                self.instance.full_clean(exclude=['password'])
            except ValidationError as e:
                self.add_error('password2', e)
                # remove the field's value from the cleaned_data
                del self.cleaned_data['password2']

    error_messages = {
        'password_mismatch': "Hesla se neshodují.",
        'password_too_short': "Heslo je příliš krátké.",
        'password_too_common': "Heslo je příliš obvyklé.",
        'password_entirely_numeric': "Heslo nesmí být zcela numerické.",
    }

