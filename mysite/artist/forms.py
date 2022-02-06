from django import forms
from .models import Artist, Images

class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = ('name', 'bio', 'poem1', 'poem2','poem3', 'profpic',
        'artist_image', 'artist_image_2', 'artist_image_3',
        'artist_altattr', 'artist_image_description', 'email', 'tags', )


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Images
        fields = ('image', )