from django.db import models
from django.contrib.auth.models import User
import re

# Create your models here.
class Tag(models.Model):
	id = models.AutoField(primary_key=True)
	tag_name = models.CharField(unique=True, max_length = 200)
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
	ctime = models.DateTimeField(auto_now = False, auto_now_add = True)
	mtime = models.DateTimeField(auto_now = True, auto_now_add = False)
	tags = models.ManyToManyField(Tag, related_name='posts')

	def __unicode__(self):
		return self.title

	def get_body_capped(self):
		return self.body[:500]

	def convert_html(self):
		html_body = self.body
		link_reg = re.compile(r'http[s]?://[^\s]+')
		img_reg = re.compile(r'.jpg|.png|.gif')
		links = link_reg.findall(html_body)
		for link in links:
			if img_reg.search(link):
				img = '<br><img border="0" src="%s"><br>' % link
				orl = re.compile(link)
				html_body = orl.sub(img, html_body)
			else:
				text = '<a href="%s">%s</a>' %(link, link)
				orl = re.compile(link)
				html_body = orl.sub(text,html_body)
		line = re.compile(r'\n+')
		html_body = line.sub('<br>',html_body)
		return html_body

	def get_tags(self):
		tags_str = ''
		first = True
		print 12
		print len(self.tags.all())
		print 34
		for tag in self.tags.all():
			print 1
			if first:
				first = False
				tags_str += tag.tag_name
			else:
				tags_str += ', '
				tags_str += tag.tag_name
		print tags_str
		return tags_str

class ImageFile(models.Model):
    image_file = models.FileField(upload_to='./')