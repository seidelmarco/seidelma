from django.db import models

from django.template.defaultfilters import slugify
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

from taggit.managers import TaggableManager


class Artist(models.Model):
    artist_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artist_owner')
    name = models.CharField('Name', max_length=200)
    bio = models.TextField(max_length=5000, null=True, blank=True)

    profpic = models.ImageField(upload_to='artist_profpic', verbose_name='Profile Pic', null=True, blank=True) #Verbose_name ist für admin-Panel-Beschriftung
    #den Bilderupload über Images lösen - DRY!
    artist_image = models.ImageField(upload_to='artist_images', verbose_name='Image 1', null=True, blank=True)
    artist_image_2 = models.ImageField(upload_to='artist_images', verbose_name='Image 2', null=True, blank=True)
    artist_image_3 = models.ImageField(upload_to='artist_images', verbose_name='Image 3', null=True, blank=True)
    artist_altattr = models.CharField('Alt Attribut', max_length=200, null=True, blank=True, default=name)
    artist_image_description = models.TextField(max_length=500, default=artist_altattr, null=True, blank=True)

    poem1 = models.TextField(null=True, blank=True)
    poem2 = models.TextField(null=True, blank=True)
    poem3 = models.TextField(null=True, blank=True)

    email = models.EmailField(max_length=254, null=True, blank=True)

    artist_comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ArtistComment',
                related_name='artist_comments_owned')

    artist_favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ArtistFav',
                related_name='artist_favorite_artists')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class ArtistCategory(models.Model):
    # darf ein Artist mehrere Kategorien haben???
    # ja - hier auch die Möglichkeit von CHOICES einbauen und Neuanlage
    catname = models.CharField('Category', max_length=200)

    tags = TaggableManager()

    def __str__(self):
        return self.catname


def get_image_filename(instance, filename):
    name = instance.artist.name
    slug = slugify(name)
    return "artist_images/%s-%s" % (slug, filename)
    #upload_to=get_image_filename, das ist ein cooler hack, um über die Funktion im imageField ein Bild zu bezeichen und upzuloaden


class Images(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, default=None)
    # es klappt in media upzuloaden ohne das ImageField zu alterieren, die Bilder
    # landen in media, weil es so in den Settings steht, nun muss ich mir noch
    # eine Lösung überlegen, wie ich in media einen Ordner artist reinbekomme
    # Update: Lösung ist einfach über upload_to einen Unterordner erschaffen, wenn
    # MEDIA_ROOT und MEDIA_URL in den settings gesetzt sind

    image = models.ImageField(upload_to='artist_images', verbose_name='Image')
    altattr = models.CharField('Alt Attribut', max_length=200, null=True, blank=True, default=artist)
    description = models.TextField(max_length=500, default=altattr, null=True, blank=True)

    def __str__(self):
        if len(self.description) < 20:
            return self.description
        return self.description[:16] + ' ...'


class Article(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    text = models.TextField()
    pic = models.ImageField(upload_to='artist_articles', null=True, blank=True)
    price = models.FloatField()
    size = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title


class ArtistComment(models.Model):
    text = models.TextField(validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")])
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 30 : return self.text
        return self.text[:27] + ' ...'


class ArtistFav(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # siehe docs.djangoproject.com/en/2.1/ref/models/options/#unique-together
    '''
    Use UniqueConstraint with the constraints option instead.

    UniqueConstraint provides more functionality than unique_together.
    unique_together may be deprecated in the future.
    '''
    class Meta:
        unique_together = ('artist', 'user')

    def __str__(self):
        return '%s likes %s'%(self.user.username, self.artist.name[:10])


