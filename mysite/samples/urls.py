from django.urls import path

from . import views

app_name = 'samples'
urlpatterns = [
    # ex: /samples/
    #path('game/<slug:guess>', views.GameView.as_view()),
    path('game', views.getform, name='getform'),
    path('loop', views.loop1, name='loop'),
    path('loop/<slug:zap>', views.loop, name='loop'),
]