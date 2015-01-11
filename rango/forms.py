# This could go within the models.py file but keeping
# forms separate keeps things a lot cleaner

from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class UserForm(forms.ModelForm):
	# This forces the form to hide the user's input into this field
	password = forms.CharField(widget=forms.PasswordInput())
	
	# recall Meta classes specify additional properties
	# about the particular modelForm class. At minimum it requires a model=
	# As of Django 1.7 either fields or exlcude are also required
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website', 'picture')

# We have to make sure that the form will provide values for all fields required by the model:
# One way to do this is use widget=forms.HiddenInput, initial=0. This will provide a value
# of 0 to the model, without allowing the user to specify a value
class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter a category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False) # The model requires the slug,
	# but since the model calculates it upon submission we don't have to do it with this form

	#An inline class to provide additional information on the form
	class Meta:
		#Provide an association between the ModelForm and a model. This is critical so
		# that django will create the form with the image of the specified model. We
		# also specify the fields to include here (in this case only name)
		model = Category
		fields = ('name',) # can't be a string, so include a comma even if only one value

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Page

	# What fields should be included i nthe form?
	# This way we don't need every field in the model to be present
	# Some fields may allow NULL values so we may not want to include them
	# For example here we hide the foreign key
	# We can either exclude the category field from the form:
	exclude = ('category')
	# or specifiy the fields to include (i.e. simply omit the category field)
	# fields = ('title','url','views')
	# ** Django requires at least one of exclude() or fields()

	# Ensures that any URLs are well-formed
	# This approach can be used to validate any form data that are passed
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		# if url is not empty and doesn't start with http, prepend it
		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url
		return cleaned_data

