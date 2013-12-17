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
from blogapp.models import Blog, Tag, Post, ImageFile
import django.contrib.auth 
from datetime import datetime

class UploadForm(forms.Form):
	title = forms.CharField()
	image_file = forms.FileField()

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
			for author_name in authors:
				author = User.objects.get(username = author_name)
				blog.users.add(author)
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
		tags = request.POST.get('tag')
		post = Post()
		post.title = post_title
		post.body = post_body
		post.ctime = datetime.now().strftime("%Y-%m-%d %H:%M")
		post.mtime = datetime.now().strftime("%Y-%m-%d %H:%M")
		post.author = request.user
		blog = Blog.objects.get(id = bid)
		post.blog = blog
		post.save()
		if tags is not None:
			print tags
			tags_list = tags.split(',')
			for tag_name in tags_list:
				tag_name = tag_name.strip()
				if len(Tag.objects.filter(tag_name = tag_name)) <= 0:
					tag = Tag()
					tag.tag_name = tag_name
					tag.save()
					post.tags.add(tag)
					post.save()
				else:
					tag = Tag.objects.get(tag_name = tag_name)
					post.tags.add(tag)
					post.save()
		return HttpResponseRedirect(reverse('blog', args=[bid]))

def post(request, bid, pid):
	data_dict = {}
	post = Post.objects.get(id=pid)
	data_dict['post'] = post
	data_dict['blog_id'] = bid
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
		post.mtime = datetime.now().strftime("%Y-%m-%d %H:%M")
		post.tags.remove()
		post.save()
		tags = request.POST.get('tag')
		if tags is not None:
			tags_list = tags.split(',')
			for tag_name in tags_list:
				tag_name = tag_name.strip()
				if len(Tag.objects.filter(tag_name = tag_name)) <= 0:
					tag = Tag()
					tag.tag_name = tag_name
					tag.save()
					post.tags.add(tag)
					post.save()
				else:
					tag = Tag.objects.get(tag_name = tag_name)
					post.tags.add(tag)
					post.save()
		return HttpResponseRedirect(reverse('blog', args=[bid]))

def tag(request, bid, tid):
	data_dict = {}
	if tid is not None:
		tag = Tag.objects.get(pk=tid)
		posts_list = tag.posts.filter(blog = bid)
		data_dict['posts'] = posts_list
		data_dict['blog_id'] = bid
	return render(request, "post_list.html", data_dict)

def upload(request):
	data_dict = {}
	return render(request, "upload.html", data_dict)

def upload_image(request):
	print 0
	if request.POST:
		print 1
		form = UploadForm(request.POST, request.FILES)
		print 2
		if form.is_valid():
			print 3
			image = ImageFile(image_file = request.FILES['image_file'])
			print image.image_file.url
			image.save()
			return HttpResponse('Succeed!')
	else:
		print 4
		return HttpResponse('Error!')
