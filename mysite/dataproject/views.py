from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views import View
from django.urls import reverse

from django.http import HttpResponse
from django.template import loader
import html

from .forms import NewEntryWatchlistForm

from .models import Keydata, NewEntryWatchlist

# Create your views here.
'''
def index(request):
    latest_keydata_list = Keydata.objects.order_by('name')
    context = {
        'latest_keydata_list': latest_keydata_list,
        }
    return render(request, 'dataproject/index.html', context)
'''

class Index(View):

    def get(self, request) :
        form = NewEntryWatchlistForm()
        latest_keydata_list = Keydata.objects.order_by('name')
        watchlist = Keydata.objects.order_by('-eps')[:8]
        ctx = { 'form' : form,
                'latest_keydata_list': latest_keydata_list,
                'watchlist': watchlist,
        }
        return render(request, 'dataproject/index.html', ctx)


    def post(self, request) :
        form = NewEntryWatchlistForm(request.POST)
        latest_keydata_list = Keydata.objects.order_by('name')
        watchlist = Keydata.objects.order_by('-eps')[:8]
        if not form.is_valid() :
            ctx = { 'form' : form,
                    'latest_keydata_list': latest_keydata_list,
                    'watchlist': watchlist,
            }
            return render(request, 'dataproject/index.html', ctx)

        # Save the form and get a model object
        newstock = form.save()
        x = reverse('dataproject:index') + '#' + str(newstock.id)
        return redirect(x)


def keydata_single_entry(request, keydata_id):
    try:
        entry = Keydata.objects.get(pk = keydata_id)
        context = {
            'entry': entry,
            }
    except Keydata.DoesNotExist:
        raise Http404('Entry does not exist')
    return render(request, 'dataproject/details.html' , context)


def keydata_details(request):
    latest_keydata_list = Keydata.objects.values().order_by('-shortrate')
    template = loader.get_template('dataproject/table.html')
    #output = ', '.join([row.name for row in latest_keydata_list])

    try:
        new_entry = Keydata(name=request.POST['name'], ticker=request.POST['ticker'], url=request.POST['url'])
        new_entry.save()
    except:
        pass
    context = {
        'latest_keydata_list': latest_keydata_list,
        }
    return HttpResponse(template.render(context, request))


def many_tables(request):
    latest_keydata_list = Keydata.objects.values().order_by('-divyield')[:8]
    new_entries = NewEntryWatchlist.objects.values().order_by('name')[:8]
    latest_keydata_list_short = Keydata.objects.values().order_by('-shortrate')[:8]
    latest_keydata_list_peratio = Keydata.objects.values().order_by('-peratio')[:8]
    ctx = { 'latest_keydata_list': latest_keydata_list,
            'new_entries': new_entries,
            'latest_keydata_list_short': latest_keydata_list_short,
            'latest_keydata_list_peratio': latest_keydata_list_peratio,
    }
    return render(request, 'dataproject/many_tables.html', ctx)

#Urls Verknüpfung - /dataproject/example
def example(request):
    form = NewEntryWatchlistForm()
    return HttpResponse(form.as_table())


# Call as dumpdata('GET', request.GET)
def dumpdata(place, data) :
    retval = ""
    if len(data) > 0 :
        retval += '<p>Incoming '+place+' data:<br/>\n'
        for key, value in data.items():
            retval += html.escape(key) + '=' + html.escape(value) + '</br>\n'
        retval += '</p>\n'
    return retval


class DumpPostView(View):  # Reusable bit...
    def post(self, request) :
        dump = dumpdata('POST', request.POST)
        ctx = {'title': 'request.POST', 'dump': dump}
        return render(request, 'dataproject/dump.html', ctx)

'''
SimpleCreate und SimpleUpdate sind Übungsviews auf dem Weg zu Validate
'''

#Urls.py Verknüpfung  - /dataproject/create
class SimpleCreate(DumpPostView):
    def get(self, request):
        form = NewEntryWatchlistForm()
        context = {'form': form}
        return render(request, 'dataproject/form.html', context)


#Urls.py Verknüpfung  - /dataproject/update
#Pulling existing data into a form

class SimpleUpdate(DumpPostView):
    def get(self, request):
        old_data = {
            'stock': 'Testaktie',
            'ticker': 'tstx',
            'url': 'https://www.enda.com',
            }
        form = NewEntryWatchlistForm(old_data)
        ctx = { 'form': form}
        return render(request, 'dataproject/form.html', ctx)


#Urls.py Verknüpfung  - /dataproject/validate
class Validate(DumpPostView):
    def get(self, request):
        old_data = {
            'name': 'Testaktie',
            'ticker': 'z. B. ZA:tstx',
            'url': 'https://www.enda.com'
            }
        form = NewEntryWatchlistForm(initial=old_data)
        ctx = { 'form': form}
        return render(request, 'dataproject/form.html', ctx)


    def post(self, request):
        form = NewEntryWatchlistForm(request.POST)
        if not form.is_valid():
            ctx = { 'form': form}
            return render(request, 'dataproject/form.html', ctx)
        # Save the data - muss hier noch programmiert werden - ACHTUNG: ich muss mit db verknüpfen Keydata - das ist oben im view keydata_details nämlich schief gegangen
        # If there are no errors, we would save the data
        x = reverse('dataproject:success')
        return redirect(x)
        #return redirect('/dataproject/success')

def success(request):
    resp = 'Thank you for the entry. We will check it and supply the keydata for this stock soon. '
    resp += """<a href="/dataproject">Go back</a>"""
    return HttpResponse(resp)



#Urls.py Verknüpfung  - /dataproject/create
class NewEntryWatchlistCreate(View):
    def get(self, request) :
        form = NewEntryWatchlistForm()
        ctx = {'form' : form}
        return render(request, 'dataproject/index.html', ctx)

    def post(self, request) :
        form = NewEntryWatchlistForm(request.POST)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, 'dataproject/index.html', ctx)

        # Save the form and get a model object
        newstock = form.save()
        x = reverse('dataproject:index') + '#' + str(newstock.id)
        return redirect(x)


#Urls.py Verknüpfung  - /dataproject/update
class NewEntryWatchlistUpdate(View):
    def get(self, request, pk) :
        oldstock = get_object_or_404(NewEntryWatchlist, pk=pk)
        form = NewEntryWatchlistForm(instance=oldstock)
        ctx = { 'form': form }
        return render(request, 'dataproject/form.html', ctx)

    def post(self, request, pk) :
        oldstock = get_object_or_404(NewEntryWatchlist, pk=pk)
        form = NewEntryWatchlistForm(request.POST, instance=oldstock)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, 'dataproject/form.html', ctx)

        editstock = form.save()
        x = reverse('dataproject:index')
        return redirect(x)

# References

# https://stackoverflow.com/questions/383944/what-is-a-python-equivalent-of-phps-var-dump





def wertepaar_keyvalue(request):
    response = """<html><body>
    <p>Your guess was """+request.GET['guess']+"""</p>
    </body></html>"""
    return HttpResponse(response)