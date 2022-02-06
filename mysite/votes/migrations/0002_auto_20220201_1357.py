# Generated by Django 3.2.3 on 2022-02-01 12:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleVotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(3, 'Title must be greater than 2 characters')])),
                ('link', models.URLField(help_text='Beginne mit https://', max_length=300)),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_votes_owner', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_votes_users', to=settings.AUTH_USER_MODEL)),
                ('userDownVotes', models.ManyToManyField(blank=True, related_name='articleDownVotes', to=settings.AUTH_USER_MODEL)),
                ('userUpVotes', models.ManyToManyField(blank=True, related_name='articleUpVotes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Artikel-Vote',
                'verbose_name_plural': 'Artikel-Votes',
            },
        ),
        migrations.DeleteModel(
            name='SmalladVotes',
        ),
    ]