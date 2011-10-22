from django.forms import ModelForm
from users.models import UserProfile

class ProfileForm(ModelForm):
  class Meta:
    model = UserProfile
    