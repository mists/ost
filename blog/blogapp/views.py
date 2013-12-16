# Create your views here.
from django import forms
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from blogapp.models import Blog
from blogapp.models import Post
import django.contrib.auth 
from datetime import datetime

def home(request):
    data_dict = {}
    blogs = Blog.objects.filter(owner = request.user)
    data_dict['blogs'] = blogs
    return render(request, 'index.html', data_dict)

def login(request):
	data_dict = {}
	return render(request, 'login.html', data_dict)

def signup(request):
	data_dict = {}
	return render(request, 'signup.html', data_dict)

def signup_user(request):
	if request.POST:
		user_name = request.POST.get('user')
		password = request.POST.get('pwd')
		if len(User.objects.filter(username = user_name)) > 0:
			return HttpResponse("User name has been taken!")
		else:
			user = User()
			user.username = user_name
			user.set_password(password)
			user.save()
			user = authenticate(username = user_name, password = password)
			django.contrib.auth.login(request, user)
			return HttpResponseRedirect(reverse('home'))

def check_login(request):
	if request.POST:
		user_name = request.POST.get('user')
		password = request.POST.get('pwd')
		user = authenticate(username = user_name, password = password)
		if user is not None and user.is_active:
			django.contrib.auth.login(request, user)
			return HttpResponseRedirect(reverse('home'))
		else:
			return HttpResponse("Wrong username or password!")

def create_blog(request):
	data_dict = {}
	user = request.user
	users = User.objects.exclude(username = user.username)
	data_dict['users'] = users
	return render(request, 'create_blog.html', data_dict)

def new_blog(request):
	if request.GET:
		blog_name = request.GET.get('blog_name')
		if len(Blog.objects.filter(blog_name = blog_name)) > 0:
			return HttpResponse("Blog name exists!")
		else:
			authors = request.GET.getlist('authors')
			print len(authors)
			print authors[0]
			blog = Blog()
			blog.blog_name = blog_name
			blog.owner = request.user
			blog.save()
			blog.users.add(*authors)
			blog.save()
			return HttpResponseRedirect(reverse('home'))

def blog(request, bid):
	data_dict = {}
	data_dict['user'] = request.user
	data_dict['blog_id'] = bid
	posts = Post.objects.filter(blog_id = bid)
	data_dict['posts'] = posts
	return render(request, "blog.html", data_dict)

def create_post(request, bid):
	data_dict = {}
	data_dict['blog_id'] = bid
	return render(request, "create_post.html", data_dict)

def new_post(request, bid):
	if request.POST:
		post_title = request.POST.get('post_title')
		post_body = request.POST.get('post_body')
		print post_body
		post = Post()
		post.title = post_title
		post.body = post_body
		post.ctime = datetime.now()
		post.mtime = datetime.now()
		post.author = request.user
		blog = Blog.objects.get(id = bid)
		post.blog = blog
		post.save()
		return HttpResponseRedirect(reverse('blog', args=[bid]))
def post(request, bid, pid):
	data_dict = {}
	post = Post.objects.get(id=pid)
	data_dict['post'] = post
	return render(request, "post.html", data_dict)

def edit_post(request, bid, pid):
	post = Post.objects.get(id = pid)
	data_dict = {}
	data_dict['post'] = post
	data_dict['bid'] = bid
	return render(request, "edit_post.html", data_dict)

def update_post(request, bid, pid):
	if request.POST:
		post = Post.objects.get(id = pid)
		post.title = request.POST.get("post_title")
		post.body = request.POST.get("post_body")
		post.mtime = datetime.now()
		post.save()
		return HttpResponseRedirect(reverse('blog', args=[bid]))

