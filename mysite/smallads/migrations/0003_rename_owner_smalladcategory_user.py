# Generated by Django 3.2.3 on 2022-01-23 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smallads', '0002_alter_smallad_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smalladcategory',
            old_name='owner',
            new_name='user',
        ),
    ]