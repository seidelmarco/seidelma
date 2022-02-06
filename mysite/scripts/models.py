from django.db import models

# Create your models here.

class Currency(models.Model):
    name = models.CharField('Name', max_length=100)
    currency = models.CharField('internationales Kürzel', max_length=100)
    rate = models.FloatField('aktuelle Rate')

    def __str__(self):
        return self.name


class Keydata(models.Model):
    name = models.CharField('Name', max_length=200, unique=True, blank=True, null=True)
    ticker = models.CharField('Tickersymbol', max_length=200, unique=True, blank=True, null=True)
    #currency_symbol = models.ForeignKey(Currency, on_delete = models.CASCADE, null=True, blank=True)
    currency_symbol = models.CharField('Currencysymbol', max_length=10, blank=True, null=True)
    #sectors = models.ManyToManyField('Sector', through='Sectored', null=True, blank=True)
    price = models.FloatField('Preis', blank=True, null=True)
    change = models.FloatField('Veränderung', blank=True, null=True)
    changepercent = models.FloatField('Veränderung in Prozent', blank=True, null=True)
    lower_day = models.FloatField('Tages-Tief', blank=True, null=True)
    upper_day = models.FloatField('Tages-Hoch', blank=True, null=True)
    sharesoutstanding = models.FloatField('Aktien in Mio', blank=True, null=True)
    publicfloat = models.FloatField('Aktien handelbar in Mio', blank=True, null=True)
    beta = models.FloatField('Beta-Faktor', blank=True, null=True)
    revperemployee = models.FloatField('Umsatz pro MA in Tsd', blank=True, null=True)
    peratio = models.FloatField('Kurs-Gewinn-Verhältnis', blank=True, null=True)
    dividend = models.FloatField('Dividende', blank=True, null=True)
    eps = models.FloatField('Gewinn je Aktie', blank=True, null=True)
    divyield = models.FloatField('Dividendenrendite', blank=True, null=True)
    exdivdate = models.CharField('Ex-Div-Datum', max_length=50, blank=True, null=True)
    shortrate = models.FloatField('Shortquote', null=True, blank=True)
    lower_52 = models.FloatField('52-Wochen-Tief', blank=True, null=True)
    upper_52 = models.FloatField('52-Wochen-Hoch', blank=True, null=True)
    url = models.URLField('URL', max_length=200, blank=True, null=True)
    note = models.CharField('Bemerkung', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class NewEntryWatchlist(models.Model):
    name = models.CharField('Name', max_length=200)
    ticker = models.CharField('Ticker', max_length=200, unique=True)
    url = models.URLField('URL', max_length=200)

    def __str__(self):
        return self.name