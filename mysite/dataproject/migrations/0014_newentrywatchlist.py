# Generated by Django 3.2.3 on 2021-07-08 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataproject', '0013_auto_20210625_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewEntryWatchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Name')),
                ('ticker', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tickersymbol')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
            ],
        ),
    ]
