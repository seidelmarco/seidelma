# Generated by Django 3.2.3 on 2022-02-01 13:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0003_auto_20220201_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlevotes',
            name='written_at',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
