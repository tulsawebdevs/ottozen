from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CommuteManager(models.Manager):
    def get_timely_commutes(self):
        now = datetime.now()
        buffer = timedelta(minutes=10)
        range_start = now - buffer
        range_end = now + buffer
        return self.filter(start_time__gte=range_start).filter(start_time__lte=range_end)

class Commute(models.Model):
    user = models.ForeignKey(User)
    start_address = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_address = models.CharField(max_length=255)

    objects = CommuteManager()

    def __unicode__(self):
        return self.user.username + ' from ' + self.start_address + ' to ' + self.end_address

class Alert(models.Model):
    user = models.ForeignKey(User)
    commute = models.ForeignKey(Commute)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    sent = models.BooleanField()

    def __unicode__(self):
        return '%s on %s' % (self.commute, self.created)
