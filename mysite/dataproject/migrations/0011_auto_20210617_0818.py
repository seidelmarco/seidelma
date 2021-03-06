# Generated by Django 3.2.3 on 2021-06-17 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataproject', '0010_auto_20210616_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Sektorname')),
            ],
        ),
        migrations.CreateModel(
            name='Sectored',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataproject.keydata')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataproject.sector')),
            ],
        ),
        migrations.AddField(
            model_name='sector',
            name='stocks',
            field=models.ManyToManyField(through='dataproject.Sectored', to='dataproject.Keydata'),
        ),
        migrations.AddField(
            model_name='keydata',
            name='sectors',
            field=models.ManyToManyField(blank=True, null=True, through='dataproject.Sectored', to='dataproject.Sector'),
        ),
    ]
