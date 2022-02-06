from django import forms
from .models import Smallad


# Create the form class.
# benutze ich ersmal nicht, weil ich nicht weiß, wie ich overriden soll
# für später zum Knobeln: in docs - sind das initial values???
class CreateForm(forms.ModelForm):

    class Meta:
        model = Smallad
        fields = ['title', 'price', 'description', 'category', 'image', 'tags']

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        if commit:
            instance.save()
            self.save_m2m()

        return instance


# strip means to remove whitespace from the beginning and the end before storing the column
class CommentForm(forms.Form):  #muss das nicht Modelform heißen?
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other