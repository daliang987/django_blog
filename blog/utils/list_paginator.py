from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def make_paginator(objects,page,num=3):
    paginator=Paginator(objects,num)

    try:
        objects_list=paginator.page(page)
    except PageNotAnInteger:
        objects_list=paginator.page(1)
    except EmptyPage:
        objects_list=paginator.page(paginator.num_pages)

    return objects_list,paginator

def paginator_data(paginator,page):

    if paginator.num_pages==1:
        return {}

    left = []
    right=[]

    left_has_more=False
    right_has_more=False

    first=False
    last=False

    try:
        page_number=int(page)
    except ValueError:
        page_number=1
    except:
        page_number=1

    total_pages=paginator.num_pages

    page_range=paginator.page_range
    if page_number==1:
        right=page_range[page_number:page_number+4]
        if right[-1]<total_pages-1:
           right_has_more=True

        if right[-1]<total_pages:
            last=True


    elif page_number==total_pages:
        left=page_range[(page_number-3) if (page_number-3>0) else 0 :page_number-1]
        if left[0]>2:
            left_has_more=True
        if left[0]>1:
            first=True

    else:
        # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
        # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]

        # 是否需要显示最后一页和最后一页前的省略号
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        # 是否需要显示第 1 页和第 1 页后的省略号
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
    }
    return data