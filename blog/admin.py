from django.contrib import admin
from .models import blog_post
# Register your models here.
@admin.register(blog_post)
class blog_postAdmin(admin.ModelAdmin):
    list_display = ('id','title','desc')