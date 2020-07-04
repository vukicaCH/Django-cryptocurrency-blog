from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def subscribe(request):
	
	if request.method == 'POST':
		email = request.POST.get('email')
		new_subscriber = Newsletter()
		new_subscriber.email = email
		new_subscriber.save()
		return HttpResponseRedirect(reverse('core:index'))
		
	return render(request, 'core/index.html')
