from django.urls import path

from . import views

app_name = 'history'

urlpatterns = [
    path('list/', views.InformationListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.InformationDetailView.as_view(), name='detail'),
]