from datetime import datetime, timedelta
import json
import re

from django.db import models
#from django.db.models.signals import post_save
from django.contrib.auth.models import User

TULSA_CLEAN_REGEX = r',\sTulsa,\sOK\s74\d{3}, USA'

class RouteManager(models.Manager):
    def get_timely_routes(self):
        now = datetime.now()
        buffer = timedelta(minutes=10)
        range_start = now - buffer
        range_end = now + buffer
        return self.filter(start_time__gte=range_start).filter(start_time__lte=range_end)


class Point(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    user = models.ForeignKey(User, related_name='point')
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=13, decimal_places=8, null=True,
                                   blank=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=8,
                                    null=True, blank=True)

    def __unicode__(self):
      return "%s's %s" % (self.user.username, self.name)


class Route(models.Model):
    user = models.ForeignKey(User, related_name='routes')
    start_time = models.TimeField(null=True)
    json = models.TextField(blank=True)

    objects = RouteManager()

    @property
    def start_address(self):
        r = json.loads(self.json)[0]
        start_address = r['legs'][0]['start_address']
        return re.sub(TULSA_CLEAN_REGEX, '', start_address)

    @property
    def end_address(self):
        r = json.loads(self.json)[0]
        end_address = r['legs'][0]['end_address']
        return re.sub(TULSA_CLEAN_REGEX, '', end_address)

    def __unicode__(self):
      return "Route %s %s" % (self.user.username, self.id)


class RoutePoint(models.Model):
    route = models.ForeignKey(Route)
    point = models.ForeignKey(Point)
    sequence = models.IntegerField()

    def __unicode__(self):
      return "Route Point %s for %s (%s)" % (self.sequence, self.route, self.point)


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
    mobile_num = models.CharField(max_length=11, default='1918.......')
    email_confirmed = models.BooleanField(default=False)
    mobile_confirmed = models.BooleanField(default=False)
    ok_to_email = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username + ' Profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

#post_save.connect(create_user_profile, sender=User)
