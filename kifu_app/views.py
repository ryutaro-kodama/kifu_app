from django.shortcuts import render

# Create your views here.

import datetime

def index(request):
    today = datetime.date.today()
    return render(request, 'index.html', {'today': today})