from django.contrib import admin

from .models import Category, Photo

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('category', 'id', 'image', 'description')

# Register your models here.

admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo, PhotoAdmin)