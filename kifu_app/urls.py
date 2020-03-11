from django.urls import path

from . import views

app_name = 'kifu_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('informationList', views.informationList, name='informationList'),
    path('informationDetail/<int:information_id>', views.informationDetail, name='informationDetail'),
]