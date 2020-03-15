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
    new_game_data = __getHistoryList()

    return redirect('add_kifu:historyList')

def __getHistoryList():
    # DB内の最新のゲームIDの取得
    try:
        last_game_id = HistoryList.objects.order_by("id").last()["game_id"]
    except:
        last_game_id = ''
        # last_game_id = 'ryu914-YMTAROO-20200314_113531'

    ghl = GetHistoryList()
    ghl.viewPage(ghl.makeHistoryListURL())
    ghl.setCookies(ghl.makeCookies())
    ghl.refresh()
    try:
        ghl.waitUntilId('history_content', 10)
    except MyNotDisplayException as e:
        print(e)
        return []

    new_game_data = []
    start = 1
    while True:
        try:
            ghl.waitUntilText('paginate_summary', f'{start}~', 10)
        except MyNotDisplayException as e:
            print(e)
            return []

        temp_game_data = ghl.getGameIds()
        for game_data in temp_game_data:
            if last_game_id == game_data[0]:
                break
            new_game_data.append(game_data)
        else:
            if ghl.hasNextPage():
                start += 10
                ghl.nextPage()
                continue
        break
    ghl.close()
    ghl.quit()

    return new_game_data

