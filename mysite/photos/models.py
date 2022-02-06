from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.conf import settings

from taggit.managers import TaggableManager

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    # SET_NULL: Set the reference to NULL (requires the field to be nullable).
    # For instance, when you delete a User, you might want to keep the comments
    # he posted on blog posts, but say it was posted by an anonymous (or deleted)
    # user. SQL equivalent: SET NULL.
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, help_text = 'Enter a category (e. g. Home & Garden)',
        validators = [MinLengthValidator(3, 'Category must be greater than 2 characters')], null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    # erstmal pro Ad nur ein Foto - später über eine Schleife mehrere Fotos uploaden
    # aber nur ein image-Feld. Geht das???
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    title = models.CharField(max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")])
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='photosapp_images', verbose_name='Photopfad und -name', null=False, blank=False)
    description = models.TextField()


    favorites = models.ManyToManyField(User, through='PhotoFav',
                related_name='favorite_photos')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    def __str__(self):
        return self.title



class PhotoComment(models.Model):
    text = models.TextField(validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")], null=True, blank=True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'


class PhotoFav(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # siehe docs.djangoproject.com/en/2.1/ref/models/options/#unique-together
    '''
    Use UniqueConstraint with the constraints option instead.

    UniqueConstraint provides more functionality than unique_together.
    unique_together may be deprecated in the future.
    '''
    class Meta:
        unique_together = ('photo', 'user')

    def __str__(self):
        return '%s likes %s'%(self.user.username, self.photo.description[:10])



