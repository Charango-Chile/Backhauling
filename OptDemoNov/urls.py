"""backhauling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.optindex, name='optindex'), #OK
    url(r'^adminlogin/$', views.adminlogin, name='adminlogin'), #OK
    url(r'^carrierlogin/$', views.carrierlogin, name='carrierlogin'), #OK
    url(r'^shipperlogin/$', views.shipperlogin, name='shipperlogin'), #OK
    url(r'^register/$', views.optregister, name='optregister'), #OK
    url(r'^register_conf/$', views.optregister_conf, name='optregister_conf'), #OK
    url(r'^login/$', views.optlogin, name='optlogin'), #OK
    url(r'^adminentry/(?P<user_name>[-\w\s]+)$', views.adminentry, name='adminentry'), #OK
    url(r'^carrierentry/(?P<user_name>[-\w\s]+)$', views.carrierentry, name='carrierentry'), #OK
    url(r'^shipperentry/(?P<user_name>[-\w\s]+)$', views.shipperentry, name='shipperentry'), #OK
    url(r'^optmatching/(?P<user_name>[-\w\s]+)$', views.optmatching, name='optmatching'), #OK
    url(r'^optmatchres/(?P<user_name>[-\w\s]+)$', views.optmatchres, name='optmatchres')  #OK
]