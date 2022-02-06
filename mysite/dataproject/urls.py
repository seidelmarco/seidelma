from django.urls import path

from . import views

app_name = 'dataproject'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('keydata/', views.keydata_details, name='keydata_details'),
    # ex: /keydata/entry/5/
    path('keydata/entry/<int:keydata_id>/', views.keydata_single_entry, name='keydata_single_entry'), #<int:keydata_id>/
    # ex: /dataproject/5/
    path('<int:keydata_id>/', views.keydata_single_entry, name='keydata_single_entry'),
    path('keydata/guess/', views.wertepaar_keyvalue, name='wertepaar_keyvalue'),
    path('example', views.example),
    path('create', views.NewEntryWatchlistCreate.as_view(), name='new_entry'),
    path('stock/<int:pk>/update', views.NewEntryWatchlistUpdate.as_view()),
    path('validate', views.Validate.as_view()),
    path('success', views.success, name='success'),
    path('many', views.many_tables, name='many_tables'),
]