from django.shortcuts import get_object_or_404, get_list_or_404, render
# from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from .models import Information

# Create your views here.

import datetime

def index(request):
    today = datetime.date.today()
    return render(request, 'index.html', {'today': today})

def informationList(request):
    data = Information.objects.all()
    return render(request, 'informationList.html', {'data': data})

def informationDetail(request, information_id):
    detail = get_object_or_404(Information, pk=information_id)
    return render(request, 'informationDetail.html', {'detail': detail})
