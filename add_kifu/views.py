from django.shortcuts import render, redirect
from .models import HistoryList
from django.views.generic import ListView, DetailView

from selenium.common.exceptions import TimeoutException

from .lib.historyList.getHistoryList import GetHistoryList
from .lib.myNotDisplayException import MyNotDisplayException

class HistoryListView(ListView):
    template_name = 'historyList.html'
    model = HistoryList
    paginate_by = 10
    # queryset = Information.objects.order_by('date')     # 今は静的にクエリを作成なのでこっちのやり方

def sync(request):
    print("OK")
    game_ids = __getHistoryList()
    return redirect('add_kifu:historyList')

def __getHistoryList():
    pass

