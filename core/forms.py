from django import forms
from .models import *

from tinymce import TinyMCE

class TinyMCEWidget(TinyMCE):
	def use_required_attribute(self, *args):
		return False
		

class PostForm(forms.ModelForm):
	text = forms.CharField(widget = TinyMCEWidget(attrs = {'required':False, 'cols':30, 'rows': 10}))
	overview = forms.CharField(widget = TinyMCEWidget(attrs = {'required':False, 'cols':30, 'rows': 10}))
	
	class Meta:
		model = Post
		fields = ['title','overview','text','featured','category','thumbnail']


