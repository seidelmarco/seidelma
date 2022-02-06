from django.contrib import admin


from unesco.models import State, Category, Region, Iso, Site

# Register your models here.

admin.site.register(State)
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(Iso)
admin.site.register(Site)