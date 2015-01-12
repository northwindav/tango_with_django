from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(selfself,request, user):
        return '/rango/'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rango/', include('rango.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^password/reset/', include('registration.backends.simple.urls'), name='password_reset'),
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
