# Generated by Django 3.2.3 on 2022-01-31 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smallads', '0004_alter_smalladfav_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='smallad',
            name='smallad_fav_sum',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]