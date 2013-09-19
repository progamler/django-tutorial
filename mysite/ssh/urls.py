from django.conf.urls import patterns, url

from ssh import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^fb/$', views.firebox, name='firebox')
)
