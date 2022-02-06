from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Photo, PhotoFav, PhotoComment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.views import View
from django.urls import reverse_lazy, reverse


from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

'''
# login/logout pages hatte ich schon für andere apps gebaut
def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)
'''

# view gallery ist so geschrieben, dass nur der reg. und eingeloggte User
# ausschließlich SEINE Kategorien und entsprechenden Fotos sieht
# nicht eingeloggte Betrachter sehen nicht einmal die Photoapp
# eingeloggte User (auch über github) sehen nichts außer ihre eigenen Uploads
'''
Für die Sellwerk-Kleinanzeigen muss ich es aber so schreiben, dass alle user
alle Anzeigen sehen können!
'''

@login_required(login_url='login')
def gallery(request):
    # der eingeloggte user wird angefragt
    user = request.user
    category = request.GET.get('category')
    # es gibt einen bug - wenn ich als User ein Foto ohne Kategorie hochlade, dann
    # ist es nicht sichtbar :(
    # ohne Kategorie kann ich es in admin auch nicht anklicken :(
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name__contains=category, category__user=user)

    favorites = []
    if request.user.is_authenticated:
        '''
        related_name='favorite_ads' aus model AD
        rows = [{'id': 2}] (A list of rows)
        '''
        rows = request.user.favorite_photos.values('id')
        favorites = [ row['id'] for row in rows]

    categories = Category.objects.filter(user=user)
    ctx = {'categories': categories, 'photos': photos, 'favorites': favorites}
    return render(request, 'photos/gallery.html', ctx)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    ctx = {'photo': photo}
    return render(request, 'photos/photo.html', ctx)


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        '''
        das ist die Lösung: nimm kein modelform,
        bestimme erst einmal welche variable category,
        dann create unten das object smalladd mit category= category
        '''
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('photos:gallery')

    ctx = {'categories': categories}
    return render(request, 'photos/add.html', ctx)


# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddPhotoFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print('Photo pk', pk)
        a = get_object_or_404(Photo, id=pk)
        fav = PhotoFav(user=request.user, photo=a)
        try:
            fav.save() #In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeletePhotoFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print('Delete pk', pk)
        a = get_object_or_404(Photo, id=pk)
        try:
            fav = PhotoFav.objects.get(user=request.user, photo=a).delete()
        except PhotoFav.DoesNotExist as e:
            pass
        return HttpResponse()





