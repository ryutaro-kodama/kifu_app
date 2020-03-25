from django.urls import path

from . import views

app_name = 'add_kifu'

urlpatterns = [
    path('historyList/', views.HistoryListView.as_view(), name='historyList'),
    path('sync/', views.sync, name='sync'),
    path('save/', views.save, name='save'),
]