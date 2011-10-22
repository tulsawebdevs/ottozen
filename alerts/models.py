from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Commute(models.Model):
    user = models.ForeignKey(User)
    start_address = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_address = models.CharField(max_length=255)

    def __unicode__(self):
        return self.user.username + ' from ' + self.start_address + ' to ' + self.end_address
