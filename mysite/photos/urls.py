from django.urls import path, reverse_lazy

from . import views

app_name = 'photos'
urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('add/', views.addPhoto, name='add'),
    path('photo/<int:pk>/', views.viewPhoto, name='photo'),
    path('photo/<int:pk>/favorite',
        views.AddPhotoFavoriteView.as_view(), name='photo_favorite'),
    path('photo/<int:pk>/unfavorite',
        views.DeletePhotoFavoriteView.as_view(), name='photo_unfavorite'),
]