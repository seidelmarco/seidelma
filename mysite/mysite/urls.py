"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.views.generic import TemplateView
from django.views import View, generic
from django.contrib.auth import views as auth_views

from django.contrib.auth import views

urlpatterns = [
    #path('', include('home.urls')),  # Change to ads.urls - meine echte Startseite is blog.urls
    #Ich möchte doch meine Blog-Auflistung als Homepage benutzen
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),  # Keep
    path('accounts/', include('django.contrib.auth.urls')),  # Keep
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # Keep
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    # Sample applications
    # nix mehr synkyndineo nennen, nur noch als Link im html, aber nicht
    # mehr als App. Die App soll business heißen, irgendwo hat sich was mit den
    # synkyndineo-tables verhakelt
    #path('synkyndineo/', include('synkyndineo.urls')),
    path('home/', include('home.urls')),
    path('hello/', include('hello.urls')),
    path('authz/', include('authz.urls')),
    #path('', TemplateView.as_view(template_name='home/main.html')),
    path('polls/', include('polls.urls')),
    path('dataproject/', include('dataproject.urls')),
    path('autos/', include('autos.urls')),
    path('cats/', include('cats.urls')),
    path('samples/', include('samples.urls')),
    path('ads/', include('ads.urls')),
    path('artist/', include('artist.urls')),
    path('photos/', include('photos.urls')),
    path('smallads/', include('smallads.urls')),
    path('votes/', include('votes.urls')),
    #path('users/', include('users.urls')),
    #path('tracks/', include('tracks.urls')),
    #path('views/', include('views.urls')),
    #path('route/', include('route.urls', namespace='nsroute')),
    #path('tmpl/', include('tmpl.urls')),
    #path('gview/', include('gview.urls')),
    #path('session/', include('session.urls')),
    #path('getpost/', include('getpost.urls')),
    #path('form/', include('form.urls')),
    #path('crispy/', include('crispy.urls')),
    #path('myarts/', include('myarts.urls')),
    #path('menu/', include('menu.urls')),
    #path('forums/', include('forums.urls')),
    #path('pics/', include('pics.urls')),
    path('favs/', include('favs.urls')),
    #path('favsql/', include('favsql.urls')),
    #path('rest/', include('rest.urls')),
    #path('usermodel/', include('usermodel.urls')),
    path('chat/', include('chat.urls')),
    #path('util/', include('util.urls')),
    #path('well/', include('well.urls')),
    #path('tagme/', include('tagme.urls')),
]


# Serve the static HTML
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Up two folders to serve "site" content
SITE_ROOT = os.path.join(BASE_DIR, 'site')

urlpatterns += [
    url(r'^site/(?P<path>.*)$', serve,
        {'document_root': os.path.join(BASE_DIR, 'site'),
         'show_indexes': True},
        name='site_path'
        ),
]

# Serve the favicon - Keep for later
urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'static'),
        }
    ),
]

urlpatterns += [
    path('apple-touch-icon.png', serve, {
            'path': 'apple-touch-icon.png',
            'document_root': os.path.join(BASE_DIR, 'static'),
        }
    ),
]

# static-function macht, dass ich alle Bilder direkt im Browser durch diese
# Eingabe finde: seidelma.pythonanywhere.com/images/foobar.jpg (Amanda.jpg i. e.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Switch to social login if it is configured - Keep for later

try:
    from . import github_settings
    social_login = 'registration/login_social.html'
    urlpatterns.insert(0,
                       path('accounts/login/', auth_views.LoginView.as_view(template_name=social_login))
                       )
    print('Using', social_login, 'as the login template')
except:
    print('Using registration/login.html as the login template')

# References

# https://docs.djangoproject.com/en/3.0/ref/urls/#include