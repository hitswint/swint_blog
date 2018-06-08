from django import forms
from django.contrib.auth.models import User
from .models import Profile


# * UserEditForm
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# * ProfileEditForm
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
