from django.contrib import admin

from .models import Question, Choice

'''
Das Problem ist, dass ich Choices wie ja und nein nicht arbiträr für
mehrere Fragen verwenden kann - dazu bräuchte ich many-to-many relations.
Der Vorteil dieser Variante ist allerdings, dass ich ja und nein pro Frage
zählen kann, was ja logisch ist
'''

class ChoiceInline(admin.TabularInline):    #Alt: StackedInline
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['question_text', 'latest_poll', 'opened']}),
        ('Date information',    {'fields': ['pub_date'], 'classes':
                                ['collapse']}),
        ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


# Register your models here.

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)