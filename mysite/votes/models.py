from django.db import models
#from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.conf import settings
from taggit.managers import TaggableManager

# Create your models here.

class ArticleVotes(models.Model):

    class Meta:
        verbose_name = 'Artikel-Vote'   #für die Admin Anzeige links im Menü
        verbose_name_plural = 'Artikel-Votes'

    title = models.CharField(max_length=200,
            validators=[MinLengthValidator(3, "Title must be greater than 2 characters")])
    link = models.URLField(max_length=300, help_text='Beginne mit https://')
    description = models.TextField()

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name='article_votes_owner')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_votes_users')

    created_at = models.DateTimeField(auto_now_add=True)
    written_at = models.DateField()

    userUpVotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='articleUpVotes')
    userDownVotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='articleDownVotes')

    tags = TaggableManager()

    def __str__(self):
        return self.title