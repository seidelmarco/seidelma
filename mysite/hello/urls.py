from django.urls import path

from . import views
#from django.views.generic import TemplateView

app_name = 'hello'
urlpatterns = [
    # ex: /hello/
    path('', views.cookie, name='cookie'),

]

