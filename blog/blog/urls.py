from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'blogapp.views.home', name='home'),
    url(r'^login/', 'blogapp.views.login', name='login'),
    url(r'^signup/', 'blogapp.views.signup', name='signup'),
    url(r'^signup_user/', 'blogapp.views.signup_user', name='signup_user'),
    url(r'^check_login/', 'blogapp.views.check_login', name='check_login'),
    url(r'^create_blog/', 'blogapp.views.create_blog', name='create_blog'),
    url(r'^upload/', 'blogapp.views.upload', name='upload'),
    url(r'^upload_image/', 'blogapp.views.upload_image', name='upload_image'),
    url(r'^new_blog/', 'blogapp.views.new_blog', name='new_blog'),
    url(r'^blogs/(\d+)/$', 'blogapp.views.blog', name='blog'),
    url(r'^blogs/(\d+)/create_post/$', 'blogapp.views.create_post', name='create_post'),
    url(r'^blogs/(\d+)/new_post/$', 'blogapp.views.new_post', name='new_post'),
    url(r'^blogs/(\d+)/posts/(\d+)/$', 'blogapp.views.post', name='post'),
    url(r'^blogs/(\d+)/posts/(\d+)/edit/$', 'blogapp.views.edit_post', name='edit_post'),
    url(r'^blogs/(\d+)/posts/(\d+)/update_post/$', 'blogapp.views.update_post', name='update_post'),
    url(r'^blogs/(\d+)/tag/(\d+)/$', 'blogapp.views.tag', name='tag'),
    # url(r'^blog/', include('blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)+ static (settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

