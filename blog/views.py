from django.shortcuts import render,HttpResponse
from blog import models


def index(request):

    entries=models.Entry.objects.all()
    return render(request,'blog/index.html',locals())

def detail(request,blog_id):
    exsits=models.Entry.objects.filter(id=blog_id).exists()
    print(exsits)
    if exsits:
        entry=models.Entry.objects.filter(id=blog_id).first()
        return render(request,'blog/detail.html',locals())
    else:
        return HttpResponse('文章不存在')