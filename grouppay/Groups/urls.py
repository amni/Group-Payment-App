from django.conf.urls import patterns, include, url

from groups import views

urlpatterns = patterns('',
   # /groups/
   url(r'^$', views.index, name='index'),

   # /groups/group_id
   url(r'^(?P<group_id>\d+)/$', views.detail, name='detail'),
   url(r'^addgroup/$', views.addgroup, name='addgroup'),
   url(r'^(?P<group_id>\d+)/addtransaction/', views.addTransaction, name='addTransaction'),
   url(r'^(?P<group_id>\d+)/addmember/email/', views.addMember_email, name='addMember_email'),
   url(r'^(?P<group_id>\d+)/addmember/username/', views.addMember_username, name='addMember_username')
)