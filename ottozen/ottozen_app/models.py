from datetime import datetime, timedelta

from django.db import models
#from django.db.models.signals import post_save
from django.contrib.auth.models import User


class RouteManager(models.Manager):
    def get_timely_commutes(self):
        now = datetime.now()
        buffer = timedelta(minutes=10)
        range_start = now - buffer
        range_end = now + buffer
        return self.filter(start_time__gte=range_start).filter(start_time__lte=range_end)


class Point(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(User)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=13, decimal_places=8, null=True,
                                   blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=8,
                                    null=True, blank=True)


class Route(models.Model):
    user = models.ForeignKey(User)
    start_time = models.TimeField(null=True)
    waypoints = models.ManyToManyField(Point, through='RoutePoints')

    objects = RouteManager()

    def __unicode__(self):
        return self.user.username + ' from ' + self.start_address + ' to ' + self.end_address


class RoutePoints(models.Model):
    route = models.ForeignKey(Route)
    point = models.ForeignKey(Point)
    sequence = models.IntegerField()


class Alert(models.Model):
    user = models.ForeignKey(User)
    route = models.ForeignKey(Route)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    sent = models.BooleanField()

    def __unicode__(self):
        return '%s on %s' % (self.route, self.created)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    mobile_num = models.CharField(max_length=10, default='918.......')
    email_confirmed = models.BooleanField(default=False)
    mobile_confirmed = models.BooleanField(default=False)
    ok_to_email = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username + ' Profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

#post_save.connect(create_user_profile, sender=User)
