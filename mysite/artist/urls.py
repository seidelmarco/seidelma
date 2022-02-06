from django.urls import path, reverse_lazy

from . import views

app_name = 'artist'
urlpatterns = [
    path('', views.gallery, name='all'),
    #path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('add/', views.addPhoto, name='add'),
    path('photo/<int:pk>/', views.viewPhoto, name='photo'),

    path('test/', views.ArtistListView.as_view(), name='test_artist_list'),
    path('test/artist/<int:pk>', views.ArtistDetailView.as_view(), name='test_artist_detail'),
    path('test/artist/create',
        views.ArtistCreateView.as_view(success_url=reverse_lazy('artist:test_artist_list')), name='test_artist_create'),
    path('test/artist/<int:pk>/update',
        views.ArtistUpdateView.as_view(success_url=reverse_lazy('artist:test_artist_list')), name='test_artist_update'),
    path('test/artist/<int:pk>/delete',
        views.ArtistDeleteView.as_view(success_url=reverse_lazy('artist:test_artist_list')), name='test_artist_confirm_delete'),
]