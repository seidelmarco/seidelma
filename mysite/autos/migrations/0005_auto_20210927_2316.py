# Generated by Django 3.2.3 on 2021-09-27 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autos', '0004_auto_20210920_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='make',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
