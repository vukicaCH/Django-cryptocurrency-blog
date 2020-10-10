from django.shortcuts import render
from .models import *
from subscribe.models import *
from .forms import *
from django.core.mail import send_mail
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def get_author(user):
	qs = Author.objects.filter(user = user)
	if qs:
		return qs[0]	
	return None


def index(request):
	featured_posts = Post.objects.filter(featured = True).order_by('id')
	
	recent_posts = Post.objects.order_by('-timestamp')
	
	crypto_posts = Post.objects.filter(category = 'CM')[:4]
	
	popular_posts = Post.objects.order_by('-views')[:4]
	
		
	context = {'featured_posts':featured_posts,
				'recent_posts':recent_posts,
				'crypto_posts':crypto_posts,
				'popular_posts':popular_posts}
	
	return render(request, 'core/index.html',context)
	
def post(request,post_id):
	popular_posts = Post.objects.order_by('-views')[:4]
	try:
		post = Post.objects.get(id = post_id)
		previous_post = Post.objects.filter(timestamp__lte = post.timestamp).exclude(id = post_id).order_by('-timestamp').first()
		next_post = Post.objects.filter(timestamp__gte = post.timestamp).exclude(id = post_id).order_by('timestamp').first()
		comments = Comment.objects.filter(post = post)	
		context = {'post':post,
				'popular_posts':popular_posts,
				'previous_post':previous_post,
				'next_post':next_post,
				'comments':comments}
	except ObjectDoesNotExist:
		return HttpResponseRedirect(reverse('core:index'))
		
	return render(request, 'core/03_single-post.html',context)
	
@login_required	
def add_comment(request,post_id):
	post = Post.objects.get(id = post_id)
	
	if request.method == 'POST':
		comment = request.POST.get('comment')
		new_comment = Comment()
		new_comment.text = comment
		new_comment.user = request.user
		new_comment.post = post
		new_comment.save()
		post.comments += 1
		post.save()
		return HttpResponseRedirect(reverse('core:post', args=[post.id]))
		
	context = {'post':post}
	return render(request, 'core/03_single-post.html', context)

@login_required	
def reply(request, post_id, comment_id):
	comment = Comment.objects.get(id = comment_id)
	post = Post.objects.get(id = post_id)
	if request.method == 'POST':
		reply_text = request.POST.get('reply')
		new_reply = Reply()
		new_reply.user = request.user
		new_reply.comment_on = comment
		new_reply.post = post
		new_reply.text = reply_text
		new_reply.save()
		comment.replies.add(new_reply)
		comment.save()
		post.comments += 1
		post.save()
		return HttpResponseRedirect(reverse('core:post',args=[post.id]))
	context = {'comment':comment,'post':post}
	return render(request, 'core/03_single-post.html',context)
	
def faq(request):
	faqs = FAQ.objects.all()
	
	context = {'faqs':faqs}
	return render(request, 'core/04_FAQs.html',context)
	
def faq_single(request, faq_id):
	faq = FAQ.objects.get(id = faq_id)
	
	context = {'faq':faq}
	return render(request, 'core/05_FAQs-single.html',context)

	
def contact(request):
	
	if request.method == 'POST':
		full_name = request.POST.get('full-name')
		subject = 'Email from ' + str(full_name) 
		email = request.POST.get('email')
		message = request.POST.get('message')
		send_mail(
				subject,
				str(message),
				str(email),
				['vuk.tsa.mes@gmail.com'],
				fail_silently=False)
		
	
	return render(request, 'core/06_contact-us.html')
	
def news(request):
	posts = Post.objects.all()
	popular_posts = Post.objects.order_by('-views')[:4]
	paginator = Paginator(posts, 4)
	
	try:
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
	except EmptyPage:
		page_obj = paginator.get_page(num_pages)
	except PageNotAnInteger:
		page_obj = paginator.get_page(1)
	
	context = {'posts':posts,
				'popular_posts':popular_posts,
				'page_obj':page_obj}
				
	return render(request, 'core/02_archive-page.html', context)
	
	
def search(request):
	posts = Post.objects.all()
	query = request.GET.get('query')
	popular_posts = Post.objects.order_by('-views')[:4]
	
	if query:
		posts = Post.objects.filter(Q(title__icontains = query) | Q(overview__icontains = query) | Q(text__icontains = query))
		
	context = {'posts':posts,
				'popular_posts':popular_posts}
				
	return render(request, 'core/search.html',context)
	
@staff_member_required	
def create(request):
	form = PostForm(request.POST, request.FILES)
	author = get_author(request.user)
	if request.method == 'POST':
		if form.is_valid():
			new_post = form.save(commit = False)
			new_post.author = author
			new_post.timestamp = timezone.now()
			new_post.save()
			return HttpResponseRedirect(reverse('core:news'))
	
	context = {'form':form}
	return render(request, 'core/create.html',context)
	
@staff_member_required		
def edit(request, post_id):
	post  = Post.objects.get(id = post_id)
	form = PostForm(instance = post)
	
	if request.method == 'POST':
		form = PostForm(request.POST,request.FILES, instance = post)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('core:post', args=[post.id]))
	context = {'form':form, 'post':post}
	return render(request, 'core/edit.html',context)

@staff_member_required	
def delete(request, post_id):
	post = Post.objects.get(id = post_id)
	post.delete()
	return HttpResponseRedirect(reverse('core:news'))
	
	
