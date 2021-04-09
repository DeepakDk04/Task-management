from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from django import forms

from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    '''
    This Form is used to create an user account
    '''
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class updateProfile(ModelForm):
    '''
    This Form is used to Update an existing user account
    '''
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
