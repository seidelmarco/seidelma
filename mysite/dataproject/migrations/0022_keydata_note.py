# Generated by Django 3.2.3 on 2021-09-04 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataproject', '0021_auto_20210901_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='keydata',
            name='note',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Bemerkung'),
        ),
    ]
