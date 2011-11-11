from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('ottozen_app.views',
    url(r'^$', 'home', name='home'),
    url(r'^commutes/add/?', 'old_add', name='old_add'),
    url(r'^account/sms$', 'account_sms_confirm', name='account_sms_confirm'),
    url(r'^account/?(?P<email>.+)?$', 'account', name='account'),
    url(r'^route/?(?P<id>\d+)?$', 'route', name='route'),
    url(r'^myroutes/?', 'myroutes', name='myroutes'),
    url(r'^phone/?', 'phone', name='phone'),
    url(r'^login/?', 'login', name='login'),
    url(r'^logout/?', 'logout', name='logout'),
    #('', include('registration.urls')),

    #('', include('registration.urls')),
    #('^accounts/profile/?', 'users.views.profile'),
    #('^commutes/add/?', 'alerts.views.add'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
