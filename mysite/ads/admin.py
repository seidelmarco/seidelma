from django.contrib import admin

from .models import Ad, Comment, Fav
# We want the admin UI to leave the picture and content_type alone

# Define the PicAdmin-class
class PicAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')

# Register your models here.

admin.site.register(Ad, PicAdmin)
admin.site.register(Comment)
admin.site.register(Fav)
