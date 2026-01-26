from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import CustomUser





# Custom registration form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'country', 'email', 'password1', 'password2']
        widgets = {
        'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border rounded-lg', 'placeholder': 'John'}),
        'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border rounded-lg', 'placeholder': 'Doe'}),
        'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border rounded-lg', 'placeholder': '+1 234 567 890'}),
        'country': forms.Select(attrs={'class': 'w-full px-4 py-3 border rounded-lg'}),
        'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 border rounded-lg', 'placeholder': 'example@email.com'}),
        'password1': forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 border rounded-lg', 'placeholder': '••••••••'}),
        'password2': forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 border rounded-lg', 'placeholder': '••••••••'}),
        }





# Custom login form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
        'placeholder': 'Username or Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
        'placeholder': '••••••••'
    }))





# Custom password change form
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
        'placeholder': 'Old Password'
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
        'placeholder': 'New Password'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600',
        'placeholder': 'Confirm New Password'
    }))