from django.conf.urls import patterns, include, url
from django.template import RequestContext

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'groups/', include('groups.urls', namespace="groups")),
    url(r'members/', include('members.urls', namespace="members")),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', 'grouppay.views.index', name="index"),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^accounts/', include('registration.backends.default.urls')),
        url(r'', include('social_auth.urls')),

    # Examples:
    # url(r'^$', 'grouppay.views.home', name='home'),
    # url(r'^grouppay/', include('grouppay.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    )
