from django.contrib import admin

from .models import Keydata, Currency, NewEntryWatchlist#, Sector, Sectored

'''
class ChoiceInline(admin.TabularInline):    #Alt: StackedInline
    model = Choice
    extra = 3
'''

class KeydataAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                  {'fields': ['name', 'ticker', 'currency_symbol',
                                'divyield', 'peratio']}),
        ('More data',    {'fields': ['price', 'change', 'changepercent', 'lower_day',
                        'upper_day', 'beta', 'dividend', 'exdivdate', 'sharesoutstanding',
                        'publicfloat', 'revperemployee',
                        'shortrate', 'lower_52', 'upper_52'], 'classes':
                        ['collapse']}),
        ('Sektoren',     {'fields': ['sector', 'subsector'], 'classes':
                        ['collapse']}),
        ('Info',        {'fields': ['note', 'url', 'dt_string'], 'classes':
                        ['collapse']}),
        ]
    #inlines = [ChoiceInline]
    list_display = ('name', 'id', 'dt_string', 'sector', 'changepercent', 'lower_day',
                    'upper_day', 'divyield', 'eps', 'peratio', 'beta',
                    'exdivdate',
                    )
    list_filter = ['sector', 'subsector']
    search_fields = ['name']


# Register your models here.

admin.site.register(Keydata, KeydataAdmin)
admin.site.register(Currency)
admin.site.register(NewEntryWatchlist)
#admin.site.register(Sector)
#admin.site.register(Sectored)
