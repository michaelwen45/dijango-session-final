from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^taller2$', views.index, name='index'),
 	url(r'^$', views.inicio),
 	url(r'^graph$', views.mygraph, name='mygraph'),
 	url(r'^grafo$', views.grafo, name='mygraph'),
 	url(r'^Taller3$', views.taller3, name='taller3'),
    url(r'^tagcloud$', views.tagcloud, name='tagcloud'),
	url(r'^punto3$', views.punto3, name='punto3'),
	

	]

