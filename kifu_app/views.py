from django.shortcuts import get_object_or_404, get_list_or_404, render
# from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.views.generic import ListView, DetailView
from .models import Information

# Create your views here.

import datetime

def index(request):
    today = datetime.date.today()
    return render(request, 'index.html', {'today': today})

class InformationListView(ListView):
    template_name = 'informationList.html'
    model = Information
    paginate_by = 10
    queryset = Information.objects.order_by('date')     # 今は静的にクエリを作成なのでこっちのやり方

    # 動的にクエリを変更したいなら、こっちのやり方
    # def get_queryset(self):
    #     return Information.objects.order_by('date')

# def informationList(request):
#     data = Information.objects.all()
#     return render(request, 'informationList.html', {'data': data})

class InformationDetailView(DetailView):
    template_name = 'informationDetail.html'
    model = Information

# def informationDetail(request, information_id):
#     detail = get_object_or_404(Information, pk=information_id)
#     return render(request, 'informationDetail.html', {'detail': detail})
