from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

# This is a decorator, which is placed directly above the function signature
@login_required
def restricted(request):
#	return HttpResponse("Since you're logged in, you can see this text!")
	return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
	logout(request) #since we know they're logged in if they can see this
	return HttpResponseRedirect('/rango/')

def user_login(request):

	# if POST, try to pull relevent info
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		# see if the combination is valid using built-in authenticate function
		user = authenticate(username=username, password=password)
		
		# if we got a user object then details were correct. IF not, no
		# user with matching credentials was found
		if user:
			if user.is_active:
				#if valid and active, we can log in (built in login() function)  and send user to the homepage
				login(request, user)
				return HttpResponseRedirect('/rango/')
			else: # inactive account. No login!
				return HttpResponse("Your Rango account is disabled.")

		else: # Wrong login details provided
			print "Invalid login! details: {0}, {1}".format(username,password)
			return HttpResponse("Invalid login details supplied.")

	# Not a POST request so display the login form. Likely be an HTTP GET
	else:
		# no context variables to pass to the template system hence the blank dictionary object
		return render(request, 'rango/login.html', {})


# Note that there are many out-of-the-box user registration modules, but
# this is a good example of how things work
def register(request):
	# A boolean value for telling the template whether the registration was successful
	# Set to False initially, code changes to true if success
	registered = False

	# If it's an HTTP POST we'll process the data
	if request.method == 'POST':
		# Grab the info from the raw form info
		# Note we make use of both UserForm and UserProfileForm
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If both are valid:
		if user_form.is_valid() and profile_form.is_valid():
			# save to db
			user = user_form.save()

			# Now has pw with the set_password method. Once hashed, update the user object
			user.set_password(user.password)
			user.save()

			# Now sort out UserProfile instance
			# Since we need to set the user attribute ourselves we set commit=FALSE
			# This delays saving the model until we're ready thus avoiding integrity issues
			profile = profile_form.save(commit=False)
			profile.user = user

			# Did the user provide a pic? If so get it from the input form and
			# put it into the UserProfile model
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now save the UserProfile model instance
			profile.save()
		
			# Update our boolean to tell the template registration was successful
			registered = True
		
		# Invalid form or forms, mistakes etc: Print problems to terminal and show to user
		else:
			print user_form.errors, profile_form.errors

	# Not a POST, so render our form using two ModelForm instances
	# These forms will be blank and ready for input
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on context
	return render(request,
		'rango/register.html',
		{'user_form':user_form, 'profile_form':profile_form,'registered':registered} )

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
