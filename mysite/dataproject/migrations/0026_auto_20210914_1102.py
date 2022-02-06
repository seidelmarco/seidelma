# Generated by Django 2.2.7 on 2021-09-14 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataproject', '0025_auto_20210914_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keydata',
            name='lower_52',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='52-Wochen-Tief'),
        ),
        migrations.AlterField(
            model_name='keydata',
            name='lower_day',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Tages-Tief'),
        ),
        migrations.AlterField(
            model_name='keydata',
            name='upper_52',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='52-Wochen-Hoch'),
        ),
        migrations.AlterField(
            model_name='keydata',
            name='upper_day',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Tages-Hoch'),
        ),
    ]
