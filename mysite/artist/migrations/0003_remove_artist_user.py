# Generated by Django 3.2.3 on 2021-12-06 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0002_alter_artist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='user',
        ),
    ]
