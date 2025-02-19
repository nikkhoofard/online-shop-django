from django import forms

from .models import User
import re

from phonenumber_field.formfields import PhoneNumberField

class SignUpForm(forms.Form):
    phone_number = PhoneNumberField()

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'type': 'tel'}
        ),
        max_length=20,
        required=False
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Basic validation:  Allow digits, spaces, +, and -
            pattern = r"^[\d\s\+\-]+$"  #Raw string to prevent escaping backslashes
            if not re.match(pattern, phone_number):
                raise forms.ValidationError("Invalid phone number format.")
        return phone_number


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'email'}
        )
    )
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'full name'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )


class ManagerLoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'type': 'tel'}
        ),
        max_length=20,
        required=False
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'password'}
        )
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Basic validation:  Allow digits, spaces, +, and -
            pattern = r"^[\d\s\+\-]+$"  #Raw string to prevent escaping backslashes
            if not re.match(pattern, phone_number):
                raise forms.ValidationError("Invalid phone number format.")
        return phone_number

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email']


