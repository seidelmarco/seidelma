from django.db import models

# Create your models here.


class Currency(models.Model):
    name = models.CharField('Name', max_length=100)
    currency = models.CharField('internationales Kürzel', max_length=100)
    rate = models.FloatField('aktuelle Rate')

    def __str__(self):
        return self.name


class Keydata(models.Model):
    SECTORS = (
        ('E', 'Energy'),
        ('M', 'Materials'),
        ('C', 'Commodities'),
        ('I', 'Industrials'),
        ('U', 'Utilities'),
        ('H', 'Healthcare'),
        ('F', 'Financials'),
        ('CD', 'Consumer Discretionary'),
        ('CS', 'Consumer Staples'),
        ('IT', 'Information Technology'),
        ('CServ', 'Communication Services'),
        ('RE', 'Real Estate'),
        )
    name = models.CharField('Name', max_length=200, unique=True, blank=True, null=True)
    ticker = models.CharField('Tickersymbol', max_length=200, unique=True, blank=True, null=True)
    sector = models.CharField('Sektor', max_length=10, choices=SECTORS, blank=True, null=True)
    subsector = models.CharField('Subsektor oder 2. Prio',max_length=10, choices=SECTORS, blank=True, null=True)
    #currency = models.ForeignKey(Currency, on_delete = models.CASCADE, verbose_name="währungssymbol" null=True, blank=True)
    currency_symbol = models.CharField('Currencysymbol', max_length=10, blank=True, null=True)
    #sector = models.ManyToManyField('Sector', through='Sectored', verbose_name="sektoren" null=True, blank=True)
    price = models.CharField('Preis', max_length=20, blank=True, null=True)
    change = models.CharField('Veränderung', max_length=20, blank=True, null=True)
    changepercent = models.CharField('Veränderung in Prozent', max_length=10, blank=True, null=True)
    lower_day = models.CharField('Tages-Tief', max_length=20, blank=True, null=True)
    upper_day = models.CharField('Tages-Hoch', max_length=20, blank=True, null=True)
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
    lower_52 = models.CharField('52-Wochen-Tief', max_length=20, blank=True, null=True)
    upper_52 = models.CharField('52-Wochen-Hoch', max_length=20, blank=True, null=True)
    url = models.URLField('URL', max_length=200, blank=True, null=True)
    note = models.CharField('Bemerkung', max_length=200, blank=True, null=True)
    fcf = models.FloatField('Free Cash Flow', default=0.0, blank=True)
    cf = models.FloatField('Cash Flow', default=0.0, blank=True)
    divfcfrate = models.FloatField('Div/FCF-Rate', default=0.0, blank=True)
    divepsrate = models.FloatField('Auszahlungsquote Div per Gewinn je Aktie', default=0.0, blank=True)
    dt_string = models.CharField('Datum und Zeit', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class NewEntryWatchlist(models.Model):
    name = models.CharField('Name', max_length=200)
    ticker = models.CharField('Ticker', max_length=200, unique=True)
    url = models.URLField('URL', max_length=200)

    def __str__(self):
        return self.name

"""
class Sector(models.Model):
    name = models.CharField('Sektorname', max_length=100)
    stocks = models.ManyToManyField(Keydata, through='Sectored')

    def __str__(self):
        return self.name


class Sectored(models.Model):
    stock = models.ForeignKey(Keydata, on_delete = models.CASCADE)
    sector =models.ForeignKey(Sector, on_delete = models.CASCADE)

    def __str__(self):
        return self.stock
"""






