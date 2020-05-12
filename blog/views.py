from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from blog import models
import markdown,pygments
from blog.utils import list_paginator
from django_comments.models import Comment

def index(request):
    print('index')
    entries=models.Entry.objects.all()
    page= request.GET.get('page',1)
    entry_list,paginator= list_paginator.make_paginator(entries,page)
    page_data=list_paginator.paginator_data(paginator,page)
    # print(locals())
    return render(request,'blog/index.html',locals())


def detail(request,blog_id):
    print('detail')
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
        # print(locals())

        comment_list=list()
        def  get_comment_list(comments):
            for comment in comments:
                comment_list.append(comment)
                children=comment.child_comment.all()
                if len(children)>0:
                    get_comment_list(children)

        top_comments=Comment.objects.filter(object_pk=blog_id,parent_comment=None,
                                            content_type__app_label='blog').order_by('-submit_date')
        get_comment_list(top_comments)
        return render(request,'blog/detail.html',locals())
    else:
        return HttpResponse('文章不存在')


def category(request,category_id):
    exists=models.Category.objects.filter(id=category_id).exists()
    if exists:
        category=models.Category.objects.filter(id=category_id).first()
        entries=models.Entry.objects.filter(category=category)
        page=request.GET.get("page",1)
        entry_list,paginator=list_paginator.make_paginator(entries,page)
        page_date=list_paginator.paginator_data(paginator,page)
        # print(locals())
        return render(request,'blog/index.html',locals())
    else:
        return HttpResponse('没有该分类')


def tag(request,tag_id):
    exists=models.Tag.objects.filter(id=tag_id).exists()
    if exists:
        tag=models.Tag.objects.filter(id=tag_id).first()
        if tag.name=='全部':
            entries=models.Entry.objects.all()
        else:
            entries=models.Entry.objects.filter(tags=tag)

        page=request.GET.get('page',1)
        entry_list,paginator=list_paginator.make_paginator(entries,page)
        page_data=list_paginator.paginator_data(paginator,page)
        # print(locals())
        return render(request,'blog/index.html',locals())
    else:
        return  HttpResponse('没有该标签')

def archives(request,year,month):
    entries=models.Entry.objects.filter(created_time__year=year,created_time__month=month)
    page=request.GET.get('page',1)
    entry_list, paginator = list_paginator.make_paginator(entries, page)
    page_data = list_paginator.paginator_data(paginator, page)
    return render(request, 'blog/index.html', locals())


def permission_denied(request):
    '''403'''
    return render(request,'blog/403.html',locals())

def page_not_find(request):
    '''404'''
    return render(request,'blog/403.html',locals())
def page_error(request):
    '''500'''
    return render(request,'blog/403.html',locals())

import requests
import json
from django.conf import  settings

def login(request):
    code=request.GET.get('code',None)
    if code is None:
        return redirect('/')

    session_token_url='https://api.weibo.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=http://127.0.0.1:8000/login&code=%s' % (settings.CLIENT_ID,settings.APP_SCRET,code)

    ret=requests.get(session_token_url)
    data=ret.text
    data_dict=json.loads(data)
    token=data_dict["access_token"]
    uid=data_dict["uid"]
    request.session["token"]=token
    request.session["uid"]=uid
    request.session["login"]=True

    user_info_url="http://api.weibo.com/2/users/show.json?access_token=%s&uid=%s" % (token,uid)
    user_info=requests.get(user_info_url)

    user_info_dict=json.loads(user_info.text)

    request.session["screen_name"]=user_info_dict["screen_name"]
    request.session["profile_image_url"]=user_info_dict["profile_image_url"]

    return redirect(request.GET.get('next','/'))


def search(request):
    keyword=request.GET.get('keyword',None)

    if not keyword:
        error_msg='请输入关键字'
        return render(request,'blog/index.html',locals())
    entries=models.Entry.objects.filter(Q(title__icontains=keyword)|Q(body__icontains=keyword)|Q(abstract__icontains=keyword))

    page=request.GET.get('page',1)
    entry_list,paginator=list_paginator.make_paginator(entries,page)
    page_data=list_paginator.paginator_data(paginator,page)

    return render(request,'blog/index.html',locals())


def logout(request):
    if request.session["login"]:
        del request.session["login"]
        del request.session["uid"]
        del request.session["token"]
        del request.session["screen_name"]
        del request.session["profile_image_url"]
        return redirect(request.GET.get('next','/'))

    else:
        return redirect('/')


from django_comments import models as comment_models

def reply(request,comment_id):
    if not request.session.get('login',None) and not request.user.is_authenticated():
        return redirect('/')

    parent_comment=get_object_or_404(Comment,id=comment_id)
    return render(request,'blog/reply.html',locals())





