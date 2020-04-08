from django.urls import path

from . import views

app_name = 'add_kifu'

urlpatterns = [
    path('', views.HistoryListView.as_view(), name='index'),
    path('sync/', views.sync, name='sync'),
    path('save/', views.save, name='save'),
]