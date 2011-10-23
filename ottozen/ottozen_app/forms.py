from django import forms
from django.forms import ModelForm
from models import UserProfile

class LoginForm(forms.Form):
  dummy_name = forms.CharField()
  password = forms.CharField()

class ProfileForm(ModelForm):
  class Meta:
    model = UserProfile
    