from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import html

# Create your views here

# Utility code - dump a dictionary
# Hilfsfunktion dumpdata für views
# call as dumpdata('GET', request.GET) oder dumpdata('POST', request.POST)

def dumpdata(place, data):
    retval = str()
    if len(data) > 0:
        retval += '<p>Incoming '+place+' data:<br/>\n'
        for key, value in data.items():
            retval += html.escape(key) + '=' + html.escape(value) + '<br/>\n'
        retval += '</p>\n'
    return retval


def getform(request):
    response = """<p>Impossible GET/POST guessing game...</p>
                <form>
                    <label for="guess">Input guess</label>
                    <input name="guess" size="40" id="guess"/>
                    <input type="submit"/>
                </form>
    """
    response += dumpdata('Get', request.GET)
    return HttpResponse(response)

class GameView(View):
    def get(self, request, guess):
        context = { 'guess' : int(guess) }
        return render(request, 'samples/cond.html', context)


def loop(request, zap):
    f = [ 'Apple', 'Orange', 'Banana', 'Strawberry', 'Lychee']
    n = ['Peanut', 'Cashew']
    x = {'fruits' : f, 'nuts' : n, 'zap' : zap}
    return render(request, 'samples/loop.html', x)


def loop1(request):
    f = [ 'Apple', 'Orange', 'Banana', 'Strawberry', 'Lychee']
    n = ['Peanut', 'Cashew']
    x = {'fruits' : f, 'nuts' : n, 'zap' : '42'}
    return render(request, 'samples/loop.html', x)