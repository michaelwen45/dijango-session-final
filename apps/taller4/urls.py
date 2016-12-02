from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^taller4_parte1$', views.taller4_parte1, name='taller4p1'),
    url(r'^taller4_parte2$', views.taller4_parte2, name='taller4p2'),
	url(r'^taller4_parte3$', views.taller4_parte3, name='taller4p3'),
	url(r'^taller4_parte4$', views.taller4_parte4, name='taller4p4'),
	url(r'^taller4_parte5$', views.relationship, name='taller4p5'),
	]
