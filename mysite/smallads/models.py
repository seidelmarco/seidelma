from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.conf import settings

from taggit.managers import TaggableManager

# Create your models here.

class SmalladCategory(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    # SET_NULL: Set the reference to NULL (requires the field to be nullable).
    # For instance, when you delete a User, you might want to keep the comments
    # he posted on blog posts, but say it was posted by an anonymous (or deleted)
    # user. SQL equivalent: SET NULL.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, help_text = 'Enter a category (e. g. Home & Garden)',
        validators = [MinLengthValidator(3, 'Category must be greater than 2 characters')], null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Smallad(models.Model):
    # erstmal pro Ad nur ein Foto - später über eine Schleife mehrere Fotos uploaden
    # aber nur ein image-Feld. Geht das???
    class Meta:
        verbose_name = 'Kleinanzeige'   #für die Admin Anzeige links im Menü
        verbose_name_plural = 'Kleinanzeigen'

    title = models.CharField(max_length=200,
            validators=[MinLengthValidator(3, "Title must be greater than 2 characters")])
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name='smallad_owner')

    category = models.ForeignKey(
        SmalladCategory, on_delete=models.SET_NULL, null=True, blank=True)
    # für später zum Knobeln: Bilder werden nicht gelöscht, wenn smallad gelöscht wird
    image = models.ImageField(upload_to='smallads_images', verbose_name='Photopfad und -name', null=False, blank=False)
    description = models.TextField()
    smallad_comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SmalladComment',
                related_name='comments_owned')

    smallad_favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='SmalladFav',
                related_name='favorite_smallads')
    #kommende Zeile wird schon von smallad_favorites ausgedrückt
    #userUpVotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='smalladUpVotes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    def __str__(self):
        return self.title



class SmalladComment(models.Model):
    text = models.TextField(validators=[MinLengthValidator(4, "Comment must be greater than 3 characters")], null=True, blank=True)
    smallad = models.ForeignKey(Smallad, on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'


class SmalladFav(models.Model):
    smallad = models.ForeignKey(Smallad, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='smallad_favs_users')
    #Alternative ausprobieren, damit jeder Visitor upvoten kann

    #smallad_visitor - also anonym - dann müssten die votes (siehe poll app) gesammelt werden und danach sortiert werden IDEE! :-)

    # siehe docs.djangoproject.com/en/2.1/ref/models/options/#unique-together
    '''
    Use UniqueConstraint with the constraints option instead.

    UniqueConstraint provides more functionality than unique_together.
    unique_together may be deprecated in the future.
    '''
    class Meta:
        unique_together = ('smallad', 'user')

    def __str__(self):
        return '%s likes %s'%(self.user.username, self.smallad.title[:20])

