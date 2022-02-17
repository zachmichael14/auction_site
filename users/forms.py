from asyncore import file_dispatcher
import email
from dataclasses import field

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pyexpat import model

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']