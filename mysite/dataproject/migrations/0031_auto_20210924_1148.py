# Generated by Django 2.2.7 on 2021-09-24 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataproject', '0030_auto_20210920_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keydata',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Name'),
        ),
    ]
