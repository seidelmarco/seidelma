# Generated by Django 3.2.3 on 2021-12-20 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0004_photocomment_photofav'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='favorites',
            field=models.ManyToManyField(related_name='favorite_photos', through='photos.PhotoFav', to=settings.AUTH_USER_MODEL),
        ),
    ]
