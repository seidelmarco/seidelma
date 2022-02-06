from django.contrib import admin

from .models import ArticleVotes


class ArticleVotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'link', 'owner')


# Register your models here.


admin.site.register(ArticleVotes, ArticleVotesAdmin)
