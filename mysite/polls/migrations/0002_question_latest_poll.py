# Generated by Django 3.2.3 on 2021-08-24 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='latest_poll',
            field=models.BooleanField(default=False, verbose_name='Eligible for latest poll'),
        ),
    ]
