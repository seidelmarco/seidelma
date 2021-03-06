# Generated by Django 3.2.3 on 2021-08-30 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataproject', '0018_alter_keydata_currency_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keydata',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='keydata',
            name='ticker',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Tickersymbol'),
        ),
    ]
