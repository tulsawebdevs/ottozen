from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('ottozen_app.views',
    url(r'^$', 'home', name='home'),
    url(r'^accounts/profile/?', 'old_profile', name='old_profile'),
    url(r'^commutes/add/?', 'old_add', name='old_add'),
    url(r'^signup/?', 'signup', name='signup'),
    url(r'^myroutes/?', 'myroutes', name='myroutes'),
    url(r'^phone/?', 'phone', name='phone'),
    url(r'^login/?', 'do_login', name='login'),
    #('', include('registration.urls')),

    #('', include('registration.urls')),
    #('^accounts/profile/?', 'users.views.profile'),
    #('^commutes/add/?', 'alerts.views.add'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
