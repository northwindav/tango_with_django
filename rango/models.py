from django.db import models
from django.template.defaultfilters import slugify # this replaces spaces with hyphens in names so that we can build clean urls

# Create your models here. For each model, a list of attributes needs to be defined
# NOTE: Primary keys do not need to be explicitely defined as it's done automatically for each model
# Since Unique=TRUE then category name must be unique
class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = "Categories"
	
	# Defining a __unicode__ method for each model is useful as
	# it will return the name rather than <Category: Category object>
	def __unicode__(self):
		return self.name

# ForeignKey creates a one-to-many relationship between Category and Page
class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title

