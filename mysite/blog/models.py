import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator


# Create your models here.



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.CharField(max_length=5000)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)


    def approve(self):
        self.approved_comment = True
        self.save()


    def __str__(self):
        return self.text


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField('modified date')
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField('Pingback Zitierhinweis bei Verlinkung')
    rating = models.IntegerField()

    def __str__(self):
        return self.headline

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)


#class HomeMessage(models.Model) :
    #text = models.TextField(max_length=500,
           # validators=[MinLengthValidator(3, "Chat must be greater than 2 characters")])

    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    #def __str__(self):
        #if len(self.text) < 15: return self.text
        #return self.text[:11] + '...'





