from django.shortcuts import render,HttpResponse
from blog import models
import markdown,pygments
from blog.utils import list_paginator

def index(request):

    entries=models.Entry.objects.all()
    page= request.GET.get('page',1)
    entry_list,paginator= list_paginator.make_paginator(entries,page)
    page_data=list_paginator.paginator_data(paginator,page)
    return render(request,'blog/index.html',locals())

def detail(request,blog_id):
    exsits=models.Entry.objects.filter(id=blog_id).exists()
    print(exsits)
    if exsits:
        entry=models.Entry.objects.filter(id=blog_id).first()
        md=markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',]
        )
        entry.body=md.convert(entry.body)
        entry.toc=md.toc
        entry.increase_visiting()
        return render(request,'blog/detail.html',locals())
    else:
        return HttpResponse('文章不存在')