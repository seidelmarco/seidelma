# Generated by Django 2.2.7 on 2021-09-14 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='make',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
