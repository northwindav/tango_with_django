from django.conf.urls import patterns, url
from rango import views


# For django to find the url mappings, this
# tupple must be called urlpatterns
urlpatterns =  patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'))

