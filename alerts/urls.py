from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('alerts.views',
    url('^commutes/add$', 'add'),
)
