from smallads.models import Smallad, SmalladCategory, SmalladComment, SmalladFav
from django.views import View
from smallads.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse

from django.db.models import Q

from smallads.forms import CreateForm, CommentForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.humanize.templatetags.humanize import naturaltime

from django.db.models import Count



class SmalladListView(OwnerListView):
    model = Smallad
    # in der urls.py heißt dieser view "all"
    # By convention:
    template_name = "smallads/smallad_list.html"

    def get(self, request):
        # mit der Suche beginnen
        strval = request.GET.get("search", False) # value search aus html
        category = request.GET.get('category')

        if category:
            category_list = SmalladCategory.objects.all().order_by('-updated_at')
            smallad_list = Smallad.objects.filter(category__name__contains=category).annotate(total=Count('smallad_favorites')).order_by('-total')

        else:
            #DAS ist die Lösung :-)
            smallad_list = Smallad.objects.all().annotate(total=Count('smallad_favorites')).order_by('-total')
            category_list = SmalladCategory.objects.all().order_by('-updated_at')

        if strval:
            # Simple title-only search
            # objects = Ad.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(price__icontains=strval), Q.OR)
            query.add(Q(category__name__icontains=strval), Q.OR) #hier mit __name, weil es ein foreign key ist
            query.add(Q(description__icontains=strval), Q.OR)
            query.add(Q(tags__name__icontains=strval), Q.OR)
            smallad_list = Smallad.objects.filter(query).select_related().order_by('-updated_at')


        smalladfav_list = list(SmalladFav.objects.all().order_by('smallad'))
        #for fav in smalladfav_list:
            #Python eine Liste durchzählen und gruppieren

        # dieser Code zeigt dem user an, welche Favoriten er hat (noch in Wunschliste umbasteln :-))
        favorites = []
        fav_count = 0
        if request.user.is_authenticated:
            '''
            related_name='favorite_ads' aus model AD
            rows = [{'id': 2}] (A list of rows)
            '''
            # related_name='favorite_smallads' aus model SmallAd
            rows = request.user.favorite_smallads.values('title')
            favorites = [ row['title'] for row in rows]

            for i in favorites:
                fav_count += 1


        # Augment the smallad_list
        for obj in smallad_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        fav_counter = [1,]

        ctx = { 'smallad_list': smallad_list, 'category_list': category_list,
                'fav_counter': fav_counter,
                'favorites': favorites,
                'smalladfav_list': smalladfav_list,
                'fav_count': fav_count,}
        return render(request, self.template_name, ctx)

# References

# https://docs.djangoproject.com/en/3.0/topics/db/queries/#one-to-many-relationships

# Note that the select_related() QuerySet method recursively prepopulates the
# cache of all one-to-many relationships ahead of time.

# sql “LIKE” equivalent in django query
# https://stackoverflow.com/questions/18140838/sql-like-equivalent-in-django-query

# How do I do an OR filter in a Django query?
# https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query

# https://stackoverflow.com/questions/1074212/how-can-i-see-the-raw-sql-queries-django-is-running



class SmalladDetailView(OwnerDetailView):
    model = Smallad
    template_name = "smallads/smallad_detail.html"

    def get(self, request, pk):
        smallad = Smallad.objects.get(id=pk)
        comments = SmalladComment.objects.filter(smallad=smallad).order_by('-updated_at')
        comment_form = CommentForm()

        favorites = []
        if request.user.is_authenticated:
            '''
            related_name='favorite_ads' aus model AD
            rows = [{'id': 2}] (A list of rows)
            '''
            # related_name='favorite_smallads' aus model SmallAd
            rows = request.user.favorite_smallads.values('id')
            favorites = [ row['id'] for row in rows]

        #funzt noch nicht
        fav_all_per_smallad = SmalladFav.objects.filter(smallad=smallad)

        ctx = {'smallad' : smallad, 'comments': comments, 'comment_form': comment_form,
               'favorites': favorites,
               'fav_all_per_smallad': fav_all_per_smallad,
              }
        return render(request, self.template_name, ctx)



'''
Dieses Probestück nehmen, um mit get_or_create zu spielen
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        ctx = {'form': form}
    return render(request, 'post_edit.html', ctx)

    ACHTUNG aufpassen: wahrscheinlich immer die related_names aus den models nehmen!
'''

# die Variante mit Modelform steht in tests.py
# diese Lösung nimmt nun die Modelform für get-request und overrides post request

class SmalladCreateView(LoginRequiredMixin, View):
    template_name = 'smallads/smallad_form.html'
    success_url = reverse_lazy('smallads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        categories = SmalladCategory.objects.all()
        ctx = {'form': form, 'categories': categories}
        return render(request, self.template_name, ctx)


    def post(self, request, pk=None):
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = SmalladCategory.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = SmalladCategory.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        smallad = Smallad.objects.create(
                title = data['title'],
                price = data['price'],
                category=category,
                description=data['description'],
                image=image,
                #Mist, die Tags werden nicht kreiert!
                tags = data['tags'],
                owner=self.request.user
            )

        return redirect(self.success_url)



# Mist: ich muss eine extra html programmieren
class SmalladUpdateView(LoginRequiredMixin, View):
    template_name = 'smallads/smallad_form_update.html'
    success_url = reverse_lazy('smallads:all')

    def get(self, request, pk):
        smallad = get_object_or_404(Smallad, id=pk, owner=self.request.user)
        form = CreateForm(instance=smallad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    # ich muss wahrscheinlich die post Funktion von oben nehmen (mit instance) und dann die html wieder umschreiben
    '''
    def post(self, request, pk):
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = SmalladCategory.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = SmalladCategory.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        smallad = Smallad.objects.update_or_create(
                title = data['title'],
                price = data['price'],
                category=category,
                description=data['description'],
                image=image,
                tags = data['tags'],
                owner=self.request.user
            )

        smallad.save()

        return redirect(self.success_url)
    '''
    def post(self, request, pk=None):
        smallad = get_object_or_404(Smallad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=smallad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)


        smallad = form.save(commit=False)
        smallad.save()
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()    # Add this
        return redirect(self.success_url)


class SmalladDeleteView(OwnerDeleteView):
    model = Smallad


def allFavs(request):
    template_name = 'smallads/smallad_allfav.html'
    smalladfav = SmalladFav.objects.all()

    ctx = {'smalladfav': smalladfav}
    return render(request, template_name, ctx)



class SmalladCommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        smallad = get_object_or_404(Smallad, id=pk)
        comment = SmalladComment(text=request.POST['comment'], owner=request.user, smallad=smallad)
        comment.save()
        return redirect(reverse('smallads:smallad_detail', args=[pk]))

class SmalladCommentDeleteView(OwnerDeleteView):
    model = SmalladComment
    template_name = "smallads/smallad_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        smallad = self.object.smallad
        return reverse('smallads:smallad_detail', args=[smallad.id])


# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class SmalladAddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print('Add pk', pk)
        a = get_object_or_404(Smallad, id=pk)
        fav = SmalladFav(user=request.user, smallad=a)
        try:
            fav.save() #In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class SmalladDeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print('Delete pk', pk)
        a = get_object_or_404(Smallad, id=pk)
        try:
            fav = SmalladFav.objects.get(user=request.user, smallad=a).delete()
        except SmalladFav.DoesNotExist as e:
            pass
        return HttpResponse()


