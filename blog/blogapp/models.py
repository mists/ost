from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
	tag_name = models.CharField(max_length = 200)
	def __unicode__(self):
		return self.tag_name

class Blog(models.Model):
	id = models.AutoField(primary_key=True)
	blog_name = models.CharField(max_length = 100)
	owner = models.ForeignKey(User, related_name="blog_owner")
	users = models.ManyToManyField(User, related_name="blog_users")
	def __unicode__(self):
		return self.blog_name

class Post(models.Model):
	blog = models.ForeignKey(Blog)
	author = models.ForeignKey(User, related_name="post_author")
	title = models.CharField(max_length = 100)
	body = models.TextField()
	ctime = models.TimeField(auto_now = False, auto_now_add = True)
	mtime = models.TimeField(auto_now = True, auto_now_add = False)
	tags = models.ManyToManyField(Tag)
	def __unicode__(self):
		return self.title




