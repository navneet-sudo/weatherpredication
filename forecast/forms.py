from django import forms

class CityForm(forms.Form):
    city = forms.CharField(max_length=100, label='Enter city')
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=None  # This removes the help text for the password
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text=None  # This removes the help text for password confirmation
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        help_texts = {
            'username': None,  # Remove the username help text if needed
        }
