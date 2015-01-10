from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	# construct a dictionary to pass to the template engine as its context.
	# Note the key boldmessage is the same as {{ boldmessage }} in the template
	context_dict = {'boldmessage': "I am bold font from the context"}

	# REturn a rendered response to send to the client
	# We make use of the shortcut function to make our lives easier
	# Note that th first parameter is the template that we wish to use
	return render(request, 'rango/index.html', context_dict)

	# This is the older response without a template
	# return HttpResponse("Rango says hey there world! <br> <a href='/rango/about'>About</a>")

def about(request):
	return HttpResponse("Rango says here is the about page. <br> <a href='/rango/'>Index</a>")
