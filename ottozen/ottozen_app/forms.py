from django import forms
from django.forms import ModelForm
from models import UserProfile

class LoginForm(forms.Form):
  dummy_name = forms.CharField(required=True)
  password = forms.CharField(required=True)


class ProfileForm(ModelForm):
  class Meta:
    model = UserProfile
    