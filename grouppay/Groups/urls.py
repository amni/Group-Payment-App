from django.conf.urls import patterns, include, url

from groups import views

urlpatterns = patterns('',
   # /groups/
   url(r'^$', views.index, name='index'),

   # /groups/group_id
   url(r'^(?P<group_id>\d+)/$', views.detail, name='detail'),
   url(r'^addgroup/$', views.addgroup, name='addgroup'),
)