from django.urls import path

from . import views

app_name = 'votes'

urlpatterns = [
    path('', views.votes, name='all'),
    #path('article/<int:pk>', views.votes, name='all'),
]