from django import forms

from .models import User
import re

from phonenumber_field.formfields import PhoneNumberField

class SignUpForm(forms.Form):
    country_code = forms.ChoiceField(
        choices=[
            ('+98', 'ایران (+98)'),
            ('+1', 'USA (+1)'),
            ('+44', 'UK (+44)'),
            ('+971', 'UAE (+971)'),
            ('+90', 'Turkey (+90)'),
            ('+49', 'Germany (+49)'),
            ('+33', 'France (+33)'),
            ('+39', 'Italy (+39)'),
            ('+7', 'Russia (+7)'),
            ('+86', 'China (+86)'),
            ('+91', 'India (+91)'),
        ],
        initial='+98',
        widget=forms.Select(attrs={'class': 'form-control country-code-select'})
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'شماره تلفن بدون کد کشور', 
                'type': 'tel',
                'dir': 'ltr'
            }
        ),
        max_length=15,
        required=True
    )
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Remove any spaces or dashes
            phone_number = re.sub(r'[\s\-]', '', phone_number)
            # Check if it contains only digits
            if not phone_number.isdigit():
                raise forms.ValidationError("شماره تلفن باید فقط شامل اعداد باشد.")
            # Check length (typical mobile number length without country code)
            if len(phone_number) < 9 or len(phone_number) > 12:
                raise forms.ValidationError("طول شماره تلفن نامعتبر است.")
        return phone_number
    
    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        phone_number = cleaned_data.get('phone_number')
        
        if country_code and phone_number:
            # Combine country code and phone number for the full international format
            full_number = f"{country_code}{phone_number}"
            cleaned_data['full_phone_number'] = full_number
            
        return cleaned_data

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'شماره تلفن بدون کد کشور', 
                'type': 'tel',
                'dir': 'ltr'
            }
        ),
        max_length=15,
        required=True
    )
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Remove any spaces or dashes
            phone_number = re.sub(r'[\s\-]', '', phone_number)
            # Check if it contains only digits
            if not phone_number.isdigit():
                raise forms.ValidationError("شماره تلفن باید فقط شامل اعداد باشد.")
            # Check length (typical mobile number length without country code)
            if len(phone_number) < 9 or len(phone_number) > 12:
                raise forms.ValidationError("طول شماره تلفن نامعتبر است.")
        return phone_number
    
    def clean(self):
        cleaned_data = super().clean()
        country_code = cleaned_data.get('country_code')
        phone_number = cleaned_data.get('phone_number')
        
        if country_code and phone_number:
            # Combine country code and phone number for the full international format
            full_number = f"{country_code}{phone_number}"
            cleaned_data['full_phone_number'] = full_number
            
        return cleaned_data

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
            attrs={
                'class': 'form-control', 
                'placeholder': '۰۹۱۲۳۴۵۶۷۸۹', 
                'type': 'tel',
                'dir': 'ltr'
            }
        ),
        max_length=20,
        required=True)
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را وارد کنید'}
        )
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # تبدیل اعداد فارسی/عربی به انگلیسی
            phone_number = ''.join([chr(ord(c) - 1728) if '۰' <= c <= '۹' else c for c in phone_number])
            
            # حذف فاصله‌ها و خط تیره‌ها
            phone_number = re.sub(r'[\s\-]', '', phone_number)
            
            # اگر با صفر شروع می‌شود، صفر را حذف کرده و +98 اضافه می‌کنیم
            if phone_number.startswith('0'):  # Changed from startsWith to startswith
                phone_number = '+98' + phone_number[1:]
            else:
                # اگر با صفر شروع نمی‌شود، بررسی می‌کنیم که آیا با +98 شروع می‌شود یا نه
                if not phone_number.startswith('+98'):  # Changed from startsWith to startswith
                    phone_number = '+98' + phone_number
            
            # بررسی اعتبار شماره تلفن
            pattern = r"^\+98\d{10}$"  # شماره تلفن ایران با فرمت +98 و 10 رقم
            if not re.match(pattern, phone_number):
                raise forms.ValidationError("لطفا یک شماره موبایل معتبر وارد کنید (مثال: ۰۹۱۲۳۴۵۶۷۸۹)")
        
        return phone_number


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email']


