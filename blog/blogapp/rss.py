from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blogapp.models import Blog, Post

class RssFeed(Feed):
    def get_object(self, request, blog_id):
        return Blog.objects.get(pk=blog_id)

    def title(self, obj):
        return obj.blog_name

    def link(self, obj):
        return reverse('blog', args=[obj.id])

    def description(self, obj):
        return obj.blog_name

    def author_name(self, obj):
        return obj.owner.username

    def author_email(self, obj):
        return obj.owner.email

    def items(self, obj):
        return Post.objects.filter(blog=obj)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        content = item.body
        ret = content[:30]
        return ret

    def item_author_name(self, item):
        return item.author.username

    def item_author_email(self, item):
        return item.author.email

    def item_pubdate(self, item):
        return item.ctime

    def item_link(self, item):
        return reverse('post', args=[item.blog.id, item.id])