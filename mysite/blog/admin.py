from django.contrib import admin

from .models import Blog, Entry, Author, Post, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(Entry)
admin.site.register(Author)

