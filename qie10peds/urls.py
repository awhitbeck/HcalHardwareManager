from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
 url(r'^$', views.index, name='index'),
 url(r'^(?P<chosen_tag>[\w\-]+)/fecrates/$',views.fecrate,name='fecrates'),
 url(r'^(?P<card_pk>[0-9]+)/(?P<chosen_tag>[\w\-]+)/peds/$',views.peds,name='peds'),
 url(r'^(?P<chosen_tag>[\w\-]+)/pmt/$',views.pmt,name='pmt'),
]
