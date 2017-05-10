from django import forms
from django.contrib.auth.models import User

class UserForm(forms.Form):
    username = forms.CharField(label='Username', min_length=4, max_length=16, required=True, error_messages={'required': 'Please enter a username', 'max_length': 'Usernames must contain 16 characters max.', 'min_length': 'Usernames must contain at least 4 characters.'})
    password = forms.CharField(label='Password', min_length=8, required=True, widget=forms.PasswordInput(), error_messages={'required': 'Please enter a password.', 'min_length': 'Passwords must contain at least 8 characters.'})
