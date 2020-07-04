from django.urls import path
from . import views
from .views import *


urlpatterns = [
	path('', views.index, name='index'),
	path('news/', views.news, name='news'),
	path('post/<post_id>', views.post, name='post'),
	path('add_comment/<post_id>', views.add_comment, name='add-comment'),
	path('post/<post_id>/reply/<comment_id>', views.reply, name = 'reply'),
	path('faq/', views.faq, name='faq'),
	path('faq-single/<faq_id>',views.faq_single, name='faq-single'),
	path('contact/', views.contact, name = 'contact'),
	path('search/', views.search, name='search'),
	path('create/', views.create, name='create'),
	path('edit/<post_id>', views.edit, name = 'edit'),
	path('delete/<post_id>', views.delete, name = 'delete')
	
]

app_name = 'core'
