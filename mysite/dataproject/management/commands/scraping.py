'''
The closepoll.py module has only one requirement – it must define a class
Command that extends BaseCommand or one of its subclasses.

The new custom command can be called using python manage.py closepoll <poll_ids>.
Achtung! Bash-Console $ nehmen, KEIN Run>>>
Das wird auch die Lösung für mein scraping script sein :-)
'''

from django.core.management.base import BaseCommand, CommandError
from urllib.request import Request, urlopen
from datetime import datetime
import time
import ssl
import sqlite3
import re
from bs4 import BeautifulSoup
#import dataproject.models.NewEntryWatchlist as NewEntryWatchlist
#import this
import sys
from dataproject.models import NewEntryWatchlist as Entry

'''
Hier die Klassen und Funktionen als Tests reinschreiben (mein scraping-Projekt),
um diese dann mit from tests import .... in views.py zu importieren

Hier 3 Dateien zusammenfassen in dieser Reihenfolge:
1. Dataproject_auf_homepage_BeautifulSoup.py
2. Dataproject_auf_homepage_marketwatch_html_main_page.txt
3. Dataproject_auf_homepage_BS4_marketwatch_parsen_exercise_file.py

Modell Tickersymbol bauen - Formular Tickersymbol - dann diese Tabelle für eine for-Schleife für scraping nutzen
Gibt es schon als class NewEntryWatchlist(models.Model):
'''

#path = '/home/seidelma/django_projects/mysite/dataproject'
#sys.path.append(path)

sys.stdout.flush()
print("About to run management command", flush=True)


class Command(BaseCommand):
    help = 'Scrapes keydata for all items in list tickers from marketwatch.com'

    def handle(self, *args, **options):
        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        SERVICE_URL = 'https://www.marketwatch.com/investing/stock/'
        #ticker = input('Enter Tickersymbol: ')
        #print(ticker)

        '''
        tickers = ['lexi?countrycode=ca', 'cmcl', 'muv2?countrycode=xe', 't',
                    'skt', 'abt', 'abbv', 'adpt', 'amgn', 'a2a?countrycode=it', 'de', 'cree', 'rblx',
                    'drd', 'amc', 'drd?countrycode=za', 'imp?countryCode=ZA', 'grmn', 'pton', 'mtn?countrycode=za', 'cvx',
                    'snh?countrycode=za', 'snh?countrycode=xe', 'jdep?countrycode=nl',]
        '''

        tickers = list()
        for line in Entry.objects.all():
            ticker = line.ticker
            tickers.append(ticker)
        print(tickers)


        # datetime object containing current date and time
        now = datetime.now()

        print("now =", now)

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)

        #url = input('Enter alternative URL or hit enter if you typed in a tickersymbol: ')

        for i in tickers:


            #if len(url) < 1: url = SERVICE_URL + i
            url = SERVICE_URL + i

            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            document = urlopen(req, context=ctx)
            html_doc = document.read()
            #print(html_doc)

            # das html Dokument für Übungszwecke lokal speichern

            def save_html(html, path):
                with open(path, 'wb') as f:
                    f.write(html)

            save_html(html_doc, 'Dataproject_auf_homepage_marketwatch_html_main_page.txt')

            soup = BeautifulSoup(html_doc, 'html.parser')
            #print(soup.prettify())

            strtitle = soup.head.title.string
            print('Title: ', strtitle)

            # als nächstes per Sicht den html-Code untersuchen - unsere Daten stehen in einem div mit
            # der Klasse class='element element--list'
            try:
                zieldiv = soup.find_all('div', {'class': 'element element--list'})
                #print('Zieldiv als Liste: ', zieldiv)
                zieldiv_als_str = zieldiv[0]

                all_li_tags = zieldiv_als_str.find_all('li')
                #print(all_li_tags)


                erster_li = all_li_tags[0]
                zweiter_li = all_li_tags[1]
                dritter_li = all_li_tags[2]
                #print(dritter_li)
                #es wird ein Objekt mit allen children gedruckt - wir haben nun small=label
                #und span=primary (value) - diese Daten brauchen wir

                # meine gesuchten Werte
                tag_small_open = erster_li.small.contents
                tag_small_open = tag_small_open[0]

                tag_small_dayrange = zweiter_li.small.contents
                tag_small_dayrange = tag_small_dayrange[0]

                tag_small_52range = dritter_li.small.contents #wirft eine Liste aus
                tag_small_52range = tag_small_52range[0]
                print(tag_small_52range)

                tag_span_open = erster_li.span.contents
                tag_span_open = tag_span_open[0]
                print('Open: ', tag_span_open)

                tag_span_dayrange = zweiter_li.span.contents
                tag_span_dayrange = tag_span_dayrange[0]
                print(tag_span_dayrange)

                tag_span_52range = dritter_li.span.contents
                tag_span_52range = tag_span_52range[0]
                print(tag_span_52range)

                # diese Technik nehmen wir unten für die Schleife, um aus den Iterationen
                # des dicts alle Key-Value-Paare auszulesen
                range_52 = dict()
                range_52[tag_small_52range] = tag_span_52range
                print(range_52)

                # nächster Schritt: aufteilen in unteren und oberen Wert mit Regex
                lower_day = re.findall('(.+[0-90-9]) ', tag_span_dayrange)
                upper_day = re.findall('- (.*.[0-90-9])', tag_span_dayrange)
                lower_day = lower_day[0]
                upper_day = upper_day[0]
                print('lower_day: ', lower_day)
                print('upper_day: ', upper_day)

                lower = re.findall('(.+[0-90-9]) ', tag_span_52range)
                upper = re.findall('- (.*.[0-90-9])', tag_span_52range)
                lower = lower[0]
                upper = upper[0]
                print('lower_52: ', lower)
                print('upper_52: ', upper)

            except:
                pass

            # Für Live-Daten wie Preis + Tickersymbol und Name finde div cx-Banner
            # und löse alle Kennzahlen mit Regex raus (BS4 geht nicht, weil es ja nur ein Tag ist.
            script_cx_banner = soup.find('script', attrs={"type": "application/ld+json"})
            #print(script_cx_banner)
            for line in script_cx_banner:
                line = line.strip()
                name = re.findall('"name":"(.+)","tickerSymbol"', line)
                ticker = re.findall('"tickerSymbol":"(.+)","exchange"', line)
                price = re.findall('"price":"(.+)","priceCurrency"', line)
                price_currency = re.findall('"priceCurrency":"(.+)","priceChange"', line)
                price_change = re.findall('"priceChange":"(.+)","priceChangePercent"', line)
                price_change_percent = re.findall('"priceChangePercent":"(.+)","quoteTime"', line)

            name = name[0]
            ticker = ticker[0]
            price = price[0]
            price_currency = (price_currency[0])
            price_change = price_change[0]
            price_change_percent = price_change_percent[0]
            print('Aus CX-Banner: ', name, ticker, price, price_currency, price_change, price_change_percent)


            # mittels Schleifen alle Key-Value-Paare aus zieldiv auslesen
            k = list()
            v = list()
            for i in zieldiv_als_str.find_all('small'):
                i = i.get_text().strip()
                k.append(i)

            for i in zieldiv_als_str.find_all('span', {"class": "primary"}):
                i = i.get_text().strip()
                v.append(i)

            #print(k, v)

            '''
            # der Code stimmt aber irgendwie habe ich die Funktion falsch gebaut
            def cleansingnulls():
                for i in v:
                    if len(i) < 1: v.remove(i)

            v.cleansingnulls()
            '''

            # Keydata als dictionary - alles aus den Schleifen in ein dict packen
            kd = dict()

            for i in range(len(k)):
                kd[k[i]] = v[i]

            #print(kd)

            # das brauchen wir eigentlich nicht - lediglich zur Darstellung:
            for key, val in list(kd.items()):
                print(key, val)

            # hier beginnen die Datenstrings zu bereinigen und in floats umwandeln:

            try:
                sharesoutstanding = float(kd['Shares Outstanding'][:-1])
            except:
                sharesoutstanding = 0.0
            print(sharesoutstanding)
            #print(type(sharesoutstanding))

            try:
                publicfloat = float(kd['Public Float'][:-1])
            except:
                publicfloat = 0.0
            print(publicfloat)

            try:
                beta = float(kd['Beta'])
            except:
                beta = 0.0
            print(beta)

            try:
                revperemployee = float(kd['Rev. per Employee'][1:-1])
            except:
                revperemployee = 0.0
            print(revperemployee)

            try:
                peratio = float(kd['P/E Ratio'])
            except:
                peratio = 0.0
            print(peratio)


            try:
                # Bsp. Verlust -$15.14 und -R6 und -€0.33 noch coden: -Z$ un Z$
                if kd['EPS'][0] == '-':
                    eps = float(kd['EPS'][2:])
                    eps = eps*-1
                else:
                    # Bsp. Gewinn $1.23
                    eps = float(kd['EPS'][1:])
            except:
                eps = kd['EPS']
            print(eps)

            try:
                divyield = float(kd['Yield'][:-1])
            except:
                divyield = 0.0
            print(divyield)

            try:
                dividend = float(kd['Dividend'][1:])
            except:
                dividend = 0.0
            print(dividend)

            try:
                shortrate = float(kd['% of Float Shorted'][:-1])
            except:
                shortrate = 0.0
            print(shortrate)

            # datetime object containing current date and time
            now = datetime.now()

            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("date and time =", dt_string)


            #fp = sys.stdout

            conn = sqlite3.connect('/home/seidelma/django_projects/mysite/db.sqlite3')
            cur = conn.cursor()
            '''
            cur.execute("""INSERT OR IGNORE INTO dataproject_keydata
                        (name, ticker, currency_symbol, price, change, changepercent, lower_day,
                        upper_day, sharesoutstanding, publicfloat, beta, revperemployee,
                        peratio, dividend, eps, divyield, exdivdate, shortrate, lower_52, upper_52, dt_string)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (name, ticker, price_currency, price, price_change, price_change_percent,
                        lower_day, upper_day, sharesoutstanding, publicfloat, beta,
                        revperemployee, peratio, dividend, eps, divyield, kd['Ex-Dividend Date'],
                        shortrate, lower, upper, dt_string)
                        )
            conn.commit()
            '''
            cur.execute('''UPDATE dataproject_keydata SET price=?, change=?, changepercent=?,
                        lower_day=?, upper_day=?, sharesoutstanding=?, publicfloat=?, beta=?,
                        revperemployee=?, peratio=?, dividend=?, eps=?, divyield=?,
                        exdivdate=?, shortrate=?, lower_52=?, upper_52=?, dt_string=? WHERE ticker=?''',
                        (price, price_change, price_change_percent, lower_day, upper_day,
                        sharesoutstanding, publicfloat, beta, revperemployee, peratio,
                        dividend, eps, divyield, kd['Ex-Dividend Date'], shortrate,
                        lower, upper, dt_string, ticker)
                        )
            conn.commit()
            #cur.close()
            #conn.close()
            #fp.flush()
            #time.sleep(1)

        cur.execute('''SELECT * FROM dataproject_keydata''')
        results = cur.fetchall()
        print(results)

        cur.close()
        conn.close()
























