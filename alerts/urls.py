from django.conf.urls.defaults import patterns, url
from django.views.generic.create_update import create_object
from alerts.models import Commute

urlpatterns = patterns('',
    url('^commutes/add$', create_object, {'model': Commute, 'login_required': True}),
)
