from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    home_address = models.CharField(max_length=255, blank=True)
    home_city = models.CharField(max_length=255, blank=True)
    mobile_num = models.CharField(max_length=10, default='9189189189')

    def __unicode__(self):
        return self.user.username + ' Profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

#post_save.connect(create_user_profile, sender=User)
