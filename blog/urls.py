
from django.conf.urls import url
from blog import views

app_name='blog'
urlpatterns = [
    url(r'^$', views.index, name='blog_index'),
    url(r'^(?P<blog_id>\d+)$',views.detail,name='blog_detail'),
    url(r'^category/(?P<category_id>\d+)$',views.category,name='blog_category'),
    url(r'^tag/(?P<tag_id>\d+)$',views.tag,name='blog_tag'),
    url(r'^archives/(?P<year>\d+)/(?P<month>\d+)$',views.archives,name='blog_archives'),
]
