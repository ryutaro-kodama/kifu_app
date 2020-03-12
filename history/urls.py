from django.urls import path

from . import views

app_name = 'history'

urlpatterns = [
    path('', views.index, name='index'),
    path('informationList', views.InformationListView.as_view(), name='informationList'),
    # path('informationList', views.informationList, name='informationList'),
    path('informationDetail/<int:pk>', views.InformationDetailView.as_view(), name='informationDetail'),
    # path('informationDetail/<int:information_id>', views.informationDetail, name='informationDetail'),
]