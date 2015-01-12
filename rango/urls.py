<<<<<<< HEAD
from django.conf.urls import patterns, url
from rango import views


# For django to find the url mappings, this
# tupple must be called urlpatterns
urlpatterns =  patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^add_category/$', views.add_category, name='add_category'),
	url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^restricted/', views.restricted, name='restricted'),
	url(r'^logout/$', views.user_logout, name='logout'),
)

||||||| merged common ancestors
=======
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

>>>>>>> 0153ebd52afe538da6d58d03fab3c967ff9aedde
