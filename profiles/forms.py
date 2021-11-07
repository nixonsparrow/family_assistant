from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def clean_phone(self):
        if self.cleaned_data.get('phone'):
            phone = str(self.cleaned_data.get('phone'))
            if phone[0:2] == '48':
                phone = phone.replace('48', '')
            if len(phone) != 9:
                raise forms.ValidationError('Phone number is not correct.')
            return phone
