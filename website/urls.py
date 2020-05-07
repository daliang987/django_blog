from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from blog.feed import LastestEntriesFeed
from blog import views as blog_views
from blog import models
from django.contrib.sitemaps import GenericSitemap,views as sitemap_views

info_dict={
    'queryset':models.Entry.objects.all(),
    'date_field':'modifyed_time'
}


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/',include('blog.urls')),
    url(r'^lastest/feed/$',LastestEntriesFeed()),
    url(r'^sitemap\.xml$',sitemap_views.sitemap,{
        'sitemaps':{
            'blog':GenericSitemap(info_dict,priority=0.6)
        }
    },name='django.contrib.sitemaps.views.sitemap'),
    url(r'^comments/',include('django_comments.urls')),
    url(r'^login/$',blog_views.login),
    url(r'^logout$',blog_views.logout),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT )


handler403=blog_views.permission_denied
handler404=blog_views.page_not_find
handler500=blog_views.page_error