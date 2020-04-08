from django.urls import path

from . import views

app_name = 'history'

urlpatterns = [
    path('', views.InformationListView.as_view(), name='index'),
    path('detail/<int:pk>/', views.InformationDetailView.as_view(), name='detail'),
]