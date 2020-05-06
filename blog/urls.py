
from django.urls import path, re_path
from blog import views
from django.conf.urls.static import static
from django.conf import settings

app_name='blog'
urlpatterns = [

    path('<int:blog_id>',views.detail,name='blog_detail'),
    path('',views.index,name='blog_index'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT )
