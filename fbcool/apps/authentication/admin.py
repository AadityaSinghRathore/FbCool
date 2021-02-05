from django.contrib import admin
from .models import Post,Comment# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)

#admin.site.register(Likes)

#class likeAdmin(admin.ModelAdmin):
 #   list_display=['likes','liked_by']

