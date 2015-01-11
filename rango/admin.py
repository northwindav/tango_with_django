from django.contrib import admin
from rango.models import Category, Page

# This will pre-populate the slug field whenever we add a new category via the admin interface. Neat
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
        list_display = ('title', 'category', 'url')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

