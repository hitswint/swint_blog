from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Profile


# * UserCreationFormCustomized
class UserCreationFormCustomized(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", 'email')
        field_classes = {'username': UsernameField}


# * UserEditForm
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


# * ProfileEditForm
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
