from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

# Create your models here.

class Message(models.Model):
    text = models.TextField(max_length=500,
           validators=[MinLengthValidator(2, "Text must be greater than 5 characters")])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'
