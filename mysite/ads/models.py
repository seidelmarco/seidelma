from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

from taggit.managers import TaggableManager


# Create your models here.

class Ad(models.Model):
    title = models.CharField(max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")])
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment',
                related_name='ad_comments_owned')
    '''
    # Diese Variante funkt. nicht in Django. Das Bild wird zwar in den Ordner
    # geladen, allerdings kann man es nicht auf der Webseite darstellen - später
    # noch in docs nachlesen TODO
    # HAHAHA es liegt an MEDIA_ROOT, MEDIA_URL und Ad.pic.url im Template ;-)
    pic = models.ImageField(upload_to='static/media/ads/images/',
            height_field=None, width_field=None, max_length=100, null=True, blank=True)
    '''

    # Picture
    picture = models.BinaryField(null=True, blank=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, blank=True,
        help_text='The MIMEType of the field')

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Fav',
                related_name='favorite_ads')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    # Shows up in the admin list
    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")])
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'


class Fav(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # siehe docs.djangoproject.com/en/2.1/ref/models/options/#unique-together
    '''
    Use UniqueConstraint with the constraints option instead.

    UniqueConstraint provides more functionality than unique_together.
    unique_together may be deprecated in the future.
    '''
    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self):
        return '%s likes %s'%(self.user.username, self.ad.title[:10])












