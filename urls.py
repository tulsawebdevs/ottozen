from django.conf.urls.defaults import patterns, include, url
import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'commute_alert.views.home', name='home'),
    # url(r'^commute_alert/', include('commute_alert.foo.urls')),
    url(r'^$', 'views.home', name='home'),
    ('', include('registration.urls')),
    ('^accounts/profile/?', 'users.views.profile'),
    ('^commutes/add/?', 'alerts.views.add'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
