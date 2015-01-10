from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from rango import views


# For django to find the url mappings, this
# tupple must be called urlpatterns
urlpatterns =  patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'))

# if DEBUG is FALSE in settings.py the ALLOWED_HOSTS need
# to be set, and the following line should be added
if not settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
