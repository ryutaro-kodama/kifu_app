from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.views.generic import ListView, DetailView
from .models import Information

# Create your views here.

class InformationListView(ListView):
    template_name = 'history/list.html'
    model = Information
    paginate_by = 10
    queryset = Information.objects.order_by('date')

class InformationDetailView(DetailView):
    template_name = 'history/detail.html'
    model = Information