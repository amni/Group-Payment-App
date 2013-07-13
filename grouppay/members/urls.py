from django.conf.urls import patterns, include, url
from django.template import RequestContext

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from members import views
urlpatterns = patterns('',
   # /groups/
   url(r'^$', views.index, name='index'),

   # /groups/group_id
   url(r'^addgroup/$', views.addgroup, name='addgroup'),
   url(r'^(?P<member_id>\d+)/addtransaction/(?P<loaning>\d+)', views.addTransaction, name='addTransaction')
   )