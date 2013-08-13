from django.conf.urls import patterns, url

from ssh import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
