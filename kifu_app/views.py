from django.shortcuts import render
from .models import Information

# Create your views here.

import datetime

def index(request):
    today = datetime.date.today()
    return render(request, 'index.html', {'today': today})

def informationList(request):
    data = Information.objects.all()
    return render(request, 'informationList.html', {'data': data})
