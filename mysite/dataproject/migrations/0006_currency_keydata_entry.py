# Generated by Django 3.2.3 on 2021-06-08 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataproject', '0005_alter_currency_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='keydata_entry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dataproject.keydata'),
        ),
    ]
