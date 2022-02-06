from django.urls import path, reverse_lazy

from . import views

app_name = 'smallads'
urlpatterns = [
    path('', views.SmalladListView.as_view(), name='all'),
    path('smallad/<int:pk>', views.SmalladDetailView.as_view(), name='smallad_detail'),
    path('smallad/create',
        views.SmalladCreateView.as_view(success_url=reverse_lazy('smallads:all')), name='smallad_create'),
    path('smallad/<int:pk>/update',
        views.SmalladUpdateView.as_view(success_url=reverse_lazy('smallads:all')), name='smallad_update'),
    path('smallad/<int:pk>/delete',
        views.SmalladDeleteView.as_view(success_url=reverse_lazy('smallads:all')), name='smallad_delete'),
    path('smallad/<int:pk>/comment',
        views.SmalladCommentCreateView.as_view(), name='smallad_comment_create'),
    path('comment/<int:pk>/delete',
        views.SmalladCommentDeleteView.as_view(success_url=reverse_lazy('smallads:all')), name='smallad_comment_delete'),
    path('smallad/<int:pk>/favorite',
        views.SmalladAddFavoriteView.as_view(), name='smallad_favorite'),
    path('smallad/<int:pk>/unfavorite',
        views.SmalladDeleteFavoriteView.as_view(), name='smallad_unfavorite'),
    path('favs',
        views.allFavs, name='smallad_allfavs'),
]