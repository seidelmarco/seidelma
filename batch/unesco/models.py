from django.db import models

# Create your models here.

class State(models.Model):
    name = models.CharField('Name Land', max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Kategorie', max_length=100)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField('Region', max_length=200)

    def __str__(self):
        return self.name


class Iso(models.Model):
    name = models.CharField('Iso-Kürzel', max_length=5)

    def __int__(self):
        return self.name


class Site(models.Model):
    name = models.CharField('Name Weltkulturerbe', max_length=500, null=True)
    description = models.TextField('Beschreibung', null=True)
    justification = models.TextField('Begründung', null=True)
    year = models.IntegerField('Aufnahmejahr', null=True, blank=True)
    longitude = models.FloatField('Längengrad', null=True)
    latitude = models.FloatField('Breitengrad', null=True)
    area_hectares = models.FloatField('Fläche in Hektar', null=True, blank=True)
    state = models.ForeignKey(State, on_delete = models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete = models.CASCADE, null=True)
    iso = models.ForeignKey(Iso, on_delete = models.CASCADE, null=True)


    def __str__(self):
        return self.name