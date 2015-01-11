from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.http import HttpResponse
from django.shortcuts import render

# This view can handle three different scenarios:
# 1. if method is POST, save form data provided by the user to the associated model, then render the homepage
# 2. if method is not POST, show a new blank form for adding a category
# 3. if there are errors, redisplay the form with error messages
def add_category(request):
	# An Http post?
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		# Have we been provided with a valid form?
		if form.is_valid():
			# save the new category to the db
			cat = form.save(commit=True)

			#now call the index() view and take the user to the homepage
			return index(request)
		else:
			# The supplied for contains errors
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details
		form = CategoryForm()

	# BAd form or for details, no form supplied..
	# Render the form with error messages (if any)
	return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
	
	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		cat = None
	
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				return category(request, category_name_slug)
				#return index(request)
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {'form':form, 'category':cat}
	return render(request, 'rango/add_page.html', context_dict)

# Basic steps for this view are:
# 1. define a context dictionary
# 2. Attempt to extract the data from the models and add it to the context dict
# 3. The category is determined by using the value passed as category_name_slug
# 4. If the vategory is found in the Category model, we then pull out the associated
#	pages and add this to the context_dict
def category(request, category_name_slug):
	context_dict = {}
	try:
		# Try to find a category name slug with the given name
		# If we can't, the get() method will raise a DoesNotExist exception
		# So the .get() method returns one model instance or raises an exceptino
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name']=category.name

		# Retrieve all of the associated pages
		# Note that the filter returns >=1 model instance
		pages = Page.objects.filter(category=category)

		# Add our results list to the template context under name pages
		context_dict['pages'] = pages

		# Also add the category object from the db to the context dict
		# We'll use this in the template to verify that the category actually exists
		context_dict['category']=category

		# Add the slug name so it's passed as well
		context_dict['category_name_slug'] = category.slug

	except Category.DoesNotExist:
		# if an exception is raised if we didn't find the specified category
		# Don't do anything: the template will display the "no category" message
		pass

	# Render the response and return to the client
	return render(request, 'rango/category.html', context_dict)

def index(request):
	# Construct a category list that queries the Category model
	# and retrives the sorted top 5 results ordered by likes
	# Pass a reference to theordered list to the dictionary, which is 
	# then passed to the template engine with the render() call
	category_list = Category.objects.order_by('-likes')[:5]
	context_dict = {'categories': category_list}

	# Construct a list of the top 5 viewed pages
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages']= page_list
	
	# REturn a rendered response to send to the client
	# We make use of the shortcut function to make our lives easier
	# Note that the second parameter is the template that we wish to use
	return render(request, 'rango/index.html', context_dict)

	# This is the older response without a template
	# return HttpResponse("Rango says hey there world! <br> <a href='/rango/about'>About</a>")

def about(request):
	context_dict = {'boldmessage': "I am a bold font for the about page"}
	return render(request, 'rango/about.html', context_dict)
	#return HttpResponse("Rango says here is the about page. <br> <a href='/rango/'>Index</a>")
