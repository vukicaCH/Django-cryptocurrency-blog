from django.urls import path
from . import views

urlpatterns = [
	path('', views.subscribe, name='sub')
	
]


app_name = 'subscribe'
