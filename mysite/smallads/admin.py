from django.contrib import admin

from .models import SmalladCategory, Smallad, SmalladComment, SmalladFav


class SmalladAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'price', 'owner', 'category', 'created_at')

class SmalladFavAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'smallad')

# Register your models here.

admin.site.register(SmalladCategory)
admin.site.register(Smallad, SmalladAdmin)
admin.site.register(SmalladComment)
admin.site.register(SmalladFav, SmalladFavAdmin)


