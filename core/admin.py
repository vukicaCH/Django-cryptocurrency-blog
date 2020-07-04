from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import *

class NewPost(admin.ModelAdmin):
	
	fieldsets = [
		("Title", {'fields': ["title"]}),
		("Overview", {"fields": ['overview']}),
        ("Text", {"fields": ['text']}),
        ("Comments", {'fields': ["comments"]}),
        ("Views", {'fields': ["views"]}),
        ("Author", {'fields': ["author"]}),
        ("Thumbnail", {'fields': ["thumbnail"]}),
        ("Categories", {'fields': ["category"]}),
        ("Featured", {'fields': ["featured"]}),
        ("Timestamp", {'fields': ["timestamp"]}),

	]
	
	formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }


# Register your models here.
admin.site.register(Author)
admin.site.register(Post,NewPost)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(FAQ)
