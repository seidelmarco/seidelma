# Generated by Django 3.2.3 on 2022-01-18 12:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0005_photo_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='photo',
            name='title',
            field=models.CharField(default='foobar', max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Title must be greater than 2 characters')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Enter a category (e. g. Home & Garden)', max_length=100, validators=[django.core.validators.MinLengthValidator(3, 'Category must be greater than 2 characters')]),
        ),
    ]
