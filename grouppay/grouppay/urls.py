from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	 # (r'^groups/(\d{3,4})/$', groups),
    # (r'^calculator/search/(\d{3,4})/(\d{2,3})/(\d{2,3})/(\d{2,3})/(\d{1,2})/$', appropriate_meal_plan),
    # Examples:
    # url(r'^$', 'grouppay.views.home', name='home'),
    # url(r'^grouppay/', include('grouppay.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
