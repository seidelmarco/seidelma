# Generated by Django 3.2.3 on 2022-01-23 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('smallads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smallad',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smallad_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
