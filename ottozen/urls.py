from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('ottozen_app.views',
    url(r'^$', 'home', name='home'),
    url(r'^accounts/profile/?', 'profile', name='old_profile'),
    url(r'^commutes/add/?', 'add', name='old_add'),
    #('', include('registration.urls')),

    #('', include('registration.urls')),
    #('^accounts/profile/?', 'users.views.profile'),
    #('^commutes/add/?', 'alerts.views.add'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
