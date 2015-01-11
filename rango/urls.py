from django.conf.urls import patterns, url
from rango import views


# For django to find the url mappings, this
# tupple must be called urlpatterns
urlpatterns =  patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
	# This regexp is a little complex:
	# r : regular expression
	# \w- : any alphanumeric characters or hyphen
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),)

