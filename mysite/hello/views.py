from django.views import generic
from django.http import HttpResponse

# Create your views here.

def cookie(request):
    print(request.COOKIES)
    oldval = request.COOKIES.get('dj4e_cookie', None)
    num_visits = request.session.get('num_visits', 0) +1
    request.session['num_visits'] = num_visits
    if num_visits > 4:
        del(request.session['num_visits'])
    resp = HttpResponse('view count=' + str(num_visits) + ' Nach 5 x refresh wird der Eintrag im dict gelöscht. Warum ist das wichtig? In a view - the dj4e_cookie value is ' + str(oldval))
    resp.set_cookie('dj4e_cookie', '8b910e56', max_age=1000)
    return resp


"""

# https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.HttpRequest.COOKIES
# HttpResponse.set_cookie(key, value='', max_age=None, expires=None, path='/',
#     domain=None, secure=None, httponly=False, samesite=None)
def cookie(request):
    print(request.COOKIES)
    oldval = request.COOKIES.get('zap', None)
    resp = HttpResponse('In a view - the zap cookie value is '+str(oldval))
    if oldval :
        resp.set_cookie('zap', int(oldval)+1) # No expired date = until browser close
    else :
        resp.set_cookie('zap', 42) # No expired date = until browser close
    resp.set_cookie('sakaicar', 42, max_age=1000) # seconds until expire
    return resp

# https://www.youtube.com/watch?v=Ye8mB6VsUHw

def sessfun(request) :
    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    if num_visits > 4 : del(request.session['num_visits'])
    resp = HttpResponse('view count='+str(num_visits))
    return resp
"""