
from django.conf.urls import url
from blog import views

app_name='blog'
urlpatterns = [
    url(r'(?P<blog_id>\d+)',views.detail,name='blog_detail'),
    url(r'^$',views.index,name='blog_index'),
]
