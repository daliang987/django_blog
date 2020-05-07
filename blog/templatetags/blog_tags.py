
from blog import models
from django import template

register=template.Library()

@register.simple_tag
def get_categories():
    return models.Category.objects.all()

@register.simple_tag
def get_entry_count_of_category(category_name):
    return models.Entry.objects.filter(category__name=category_name).count()


@register.simple_tag
def archives():
    return models.Entry.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_entry_count_of_date(year,month):
    return models.Entry.objects.filter(created_time__year=year,created_time__month=month).count()

@register.simple_tag
def get_tags():
    return models.Tag.objects.all()

@register.simple_tag
def get_entry_count_of_tags(tag_name):
    return models.Entry.objects.filter(tags__name=tag_name).count()