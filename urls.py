from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'commute_alert.views.home', name='home'),
    # url(r'^commute_alert/', include('commute_alert.foo.urls')),
    ('', include('registration.urls')),
    ('', include('alerts.urls')),
    ('^accounts/profile/?', 'users.views.profile'),
    ('^login/?'), 'users.views.login'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
