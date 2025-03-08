from django import forms
from django.contrib.auth.forms import UserCreationForm
from disast.models import User

from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=150
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class CitizenSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AgencySignupForm(UserCreationForm):
    agency_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
from .models import Disaster

class DisasterForm(forms.ModelForm):
    class Meta:
        model = Disaster
        fields = ['title','location', 'description', 'link', 'category', 'severity', 'date','date_reported']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }