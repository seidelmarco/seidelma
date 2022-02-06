from django.contrib import admin

from .models import Artist, Images, Article
# We want the admin UI to leave the picture and content_type alone

# Define the PicAdmin-class
#class PicAdmin(admin.ModelAdmin):
    #exclude = ('picture', 'content_type')

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')

# Register your models here.

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Images)
admin.site.register(Article)