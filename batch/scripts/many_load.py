import csv #https://docs.python.org/3/library/csv.html
from tqdm import tqdm


# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

"""
Dieses Skript lädt csv-Daten in ein bestehendes DB-Model
"""

from unesco.models import State, Category, Region, Iso, Site


def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')
    reader = csv.reader(fhand)
    next(reader) # Advance past the header

    Category.objects.all().delete()
    State.objects.all().delete()
    Region.objects.all().delete()
    Iso.objects.all().delete()
    Site.objects.all().delete()

    # Format
    # name,description,justification,year,longitude,latitude,area_hectares,category,state,region,iso

    # Cultural Landscape and Archaeological Remains of the Bamiyan Valley, <p>descri</p>, <p>justi</p>, 2003,67,82525,34,84694,158,9265,Cultural,Afghanistan,Asia and the Pacific,af



    for row in tqdm(reader):
        #print(row)

        """
        mit der folgenden Zeile Code werden nur die Zeilen für die kleinen FK-Tabellen befüllt
        This is meant as a shortcut to boilerplatish code. For example:

        try:
            obj = Person.objects.get(first_name='John', last_name='Lennon')
        except Person.DoesNotExist:
            obj = Person(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
            obj.save()
        This pattern gets quite unwieldy as the number of fields in a model goes up. The above example can be rewritten using get_or_create() like so:

        obj, created = Person.objects.get_or_create(first_name='John', last_name='Lennon',
                          defaults={'birthday': date(1940, 10, 9)})
        """

        c, created = Category.objects.get_or_create(name=row[7])
        s, created = State.objects.get_or_create(name=row[8])
        r, created = Region.objects.get_or_create(name=row[9])
        iso, created = Iso.objects.get_or_create(name=row[10])


        #try:
        #    area = float(row[6])
        #except:
        #    area = None

        #besser - expliziter für area-Zellen, die einen leeren string enthalten
        area = float(row[6]) if row[6] else None

        """
        die Haupttabelle zieht sich die eineindeutigen Zellen aus der csv, die Extratabellen werden nur über die FK, also die oben geschaffenen
        Objekte/Instanzen referenziert
        """
        site = Site(name=row[0], description=row[1], justification=row[2], year=row[3], longitude=row[4], latitude=row[5], area_hectares=area, category=c, state=s, region=r, iso=iso)
        site.save()