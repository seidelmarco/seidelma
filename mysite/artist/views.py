from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ImageForm, ArtistForm
from .models import Images, Artist, ArtistComment

from django.views import View
from artist.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView


from django.urls import reverse_lazy, reverse

from django.db.models import Q


from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.humanize.templatetags.humanize import naturaltime


#'''
class ArtistListView(OwnerListView):
    # als erstes alle Views mit request-response-cycle zum Laufen bringen, jedem ein test-html zuweisen und in urls verknüpfen
    model = Artist
    template_name = 'artist/test_artist_list.html'

    def get(self, request):
        artist_list = Artist.objects.all().order_by('-updated_at')[:10] #später nach Favoriten ordnen
        ctx = { 'artist_list': artist_list, }
        return render(request, self.template_name, ctx)


class ArtistDetailView(OwnerDetailView):
    model = Artist
    template_name = "artist/test_artist_detail.html"

    def get(self, request, pk):
        artist = Artist.objects.get(id=pk)
        #comments = #Comment.objects.filter(artist=artist).order_by('-updated_at')
        #comment_form = CommentForm()
        ctx = {'artist' : artist,}
        return render(request, self.template_name, ctx)


class ArtistCreateView(LoginRequiredMixin, View):
    #model = Artist
    template_name = "artist/test_artist_form.html"
    success_url = reverse_lazy('artist:test_artist_list')

    def get(self, request, pk=None):
        form = ArtistForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = ArtistForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        artist = form.save(commit=False)
        artist.artist_owner = self.request.user
        artist.save()
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()    # Add this
        return redirect(self.success_url)


class ArtistUpdateView(LoginRequiredMixin, View):

    template_name = 'artist/test_artist_form.html'
    success_url = reverse_lazy('artist:test_artist_list')

    def get(self, request, pk):
        artist = get_object_or_404(Artist, id=pk, artist_owner=self.request.user)
        form = ArtistForm(instance=artist)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        artist = get_object_or_404(Artist, id=pk, artist_owner=self.request.user)
        form = ArtistForm(request.POST, request.FILES or None, instance=artist)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        artist = form.save(commit=False)
        artist.save()
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()    # Add this

        return redirect(self.success_url)


class ArtistDeleteView(OwnerDeleteView):
    model = Artist
    template_name = 'artist/test_artist_confirm_delete.html'
    success_url = reverse_lazy('artist:test_artist_list')
#'''


def gallery(request):
    artist = request.GET.get('artist')
    if artist == None:
        photos = Images.objects.all()
    else:
        photos = Images.objects.filter(artist__name=artist)

    artists = Artist.objects.all()

    ctx = {'artists': artists,
            'photos': photos,
            }
    return render(request, 'artist/artist_main_list.html', ctx)


#Variante, die funktioniert
def viewPhoto(request, pk):
    photos = Images.objects.get(id=pk)
    ctx = {
            'photos': photos,
            }
    #return render(request, 'artist/artist_detail.html', ctx)
    return render(request, 'artist/photo.html', ctx)

'''
class ArtistDetailView(DetailView):
    model = Artist
    template_name = "artist/artist_detail.html"
    #template_name = "artist/photo.html"


    def get(self, request, pk):
        artist = Artist.objects.get(id=pk)
        #images = Images.objects.get(id=pk)
        comments = ArtistComment.objects.filter(artist=artist).order_by('-updated_at')
        #comment_form = CommentForm()
        ctx = {'artist' : artist, 'comments': comments }
        return render(request, self.template_name, ctx)
'''

@login_required
def addPhoto(request):
    artists = Artist.objects.all()
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['artist'] != 'none':
            artist = Artist.objects.get(id=data['artist'])
        elif data['artist_new'] != '':
            artist, created = Artist.objects.get_or_create(name=data['artist_new'])
        else:
            artist = None

        for image in images:
            photo = Images.objects.create(
                artist=artist,
                description=data['description'],
                image=image,
                )

        return redirect('artist:all')

    ctx = {'artists': artists,
            }
    return render(request, 'artist/artist_form.html', ctx)




'''
# Variante für die Benutzung von Formsets
@login_required
def post(request):

    ImageFormSet = modelformset_factory(Images,
                                        form=ImageForm, extra=6)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        artistForm = ArtistForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())


        if artistForm.is_valid() and formset.is_valid():
            artist_form = artistForm.save(commit=False)
            artist_form.user = request.user
            artist_form.save()

            for form in formset.cleaned_data:
                #this helps to not crash if the user
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(artist=artist_form, image=image)
                    photo.save()
            # use django messages framework
            messages.success(request,
                             "Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(artistForm.errors, formset.errors)
    else:
        artistForm = ArtistForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'artist/artist_form.html',
                  {'artistForm': artistForm, 'formset': formset})
'''
