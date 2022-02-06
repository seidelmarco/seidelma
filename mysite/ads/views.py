from ads.models import Ad, Comment, Fav
from django.views import View
from ads.owner import OwnerListView, OwnerDetailView, OwnerDeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse

from django.db.models import Q

from ads.forms import CreateForm, CommentForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.humanize.templatetags.humanize import naturaltime

from ads.utils import dump_queries


class AdListView(OwnerListView):
    model = Ad
    # in der urls.py heißt dieser view "all"
    # By convention:
    template_name = "ads/ad_list.html"

    def get(self, request):
        # mit der Suche beginnen
        strval = request.GET.get("search", False)
        if strval:
            # Simple title-only search
            # objects = Ad.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            query.add(Q(tags__name__icontains=strval), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else:
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        favorites = []
        if request.user.is_authenticated:
            '''
            related_name='favorite_ads' aus model AD
            rows = [{'id': 2}] (A list of rows)
            '''
            rows = request.user.favorite_ads.values('id')
            favorites = [ row['id'] for row in rows]

        # Augment the ad_list
        for obj in ad_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = { 'ad_list': ad_list, 'favorites': favorites, 'search': strval}
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

'''
class AdListView(OwnerListView):
    model = Ad
    # in der urls.py heißt dieser view "all"
    # By convention:
    template_name = "ads/ad_list.html"

    def get(self, request):
        ad_list = Ad.objects.all()
        favorites = []
        if request.user.is_authenticated:
'''
'''
            related_name='favorite_ads' aus model AD
            rows = [{'id': 2}] (A list of rows)
'''
'''
            rows = request.user.favorite_ads.values('id')
            favorites = [ row['id'] for row in rows]
        ctx = { 'ad_list': ad_list, 'favorites': favorites}
        return render(request, self.template_name, ctx)
'''



class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"

    #in diese comment get-request muss natürlich auch noch meine Bilderrequest rein,
    #da diese def get die OwnerDetailView überschreibt

    def get(self, request, pk):
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        ctx = {'ad' : ad, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, ctx)



'''
(3) Take a look at pics/views.py and adapt the patterns in PicCreateView and
PicUpdateView and replace the code for AdCreateView and AdUpdateView in ads/views.py.
These new views don't inherit from owner.py because they manage the owner
column in the get() and post() methods.

Ich schreibe also Teile aus owner.py wieder zurück in diese Views. Für folgende
Projekte merken, dass ich eigentlich auch alles in owner.py händeln kann, oder?
'''

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')   #einfach nur der AdListView

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()    # Add this
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()
        # https://django-taggit.readthedocs.io/en/latest/forms.html#commit-false
        form.save_m2m()    # Add this

        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response

# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print('Add pk', pk)
        a = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=a)
        try:
            fav.save() #In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print('Delete pk', pk)
        a = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=a).delete()
        except Fav.DoesNotExist as e:
            pass
        return HttpResponse()

