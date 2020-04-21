from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.views.generic import ListView, DetailView
from .models import Information

from lib.shogitime.convert2shogitime import convert2shogitime

# Create your views here.

class InformationListView(ListView):
    template_name = 'history/index.html'
    model = Information
    paginate_by = 10
    queryset = Information.objects.order_by('date')

class InformationDetailView(DetailView):
    template_name = 'history/detail.html'
    model = Information

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filename = "20200310_141940-ryu914-hiroton777.kifu"
        context["data"] = convert2shogitime(filename)
        return context
