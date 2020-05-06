from django.contrib import admin
from blog import models


class EntryAdmin(admin.ModelAdmin):
    list_display=['title','author','visiting','created_time','modifyed_time']

admin.site.register(models.Category)
admin.site.register(models.Entry,EntryAdmin)
admin.site.register(models.Tag)

