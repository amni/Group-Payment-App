from django.conf.urls import patterns, include, url

from groups import views

urlpatterns = patterns('',
   # /me
   url(r'^$', views.index, name='index'),
)