# Generated by Django 3.2.3 on 2021-12-15 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_auto_20211209_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='photosapp_images', verbose_name='Photopfad und -name'),
        ),
    ]
