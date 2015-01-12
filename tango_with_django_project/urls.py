from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    (r'^accounts/', include('registration.backends.simple.urls')),
)

# this combined with the settings module allows us to access
# settings.py. We append this pattern so that if DEBUG=TRUE
# then this pattern match will allow us to directly view media
if settings.DEBUG:
	urlpatterns += patterns(
		'django.views.static',
		(r'^media/(?P<path>.*)',
		'serve',
		{'document_root':settings.MEDIA_ROOT}), )
