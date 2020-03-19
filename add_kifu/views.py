from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.utils.timezone import make_aware
from .models import HistoryList

from selenium.common.exceptions import TimeoutException
import datetime as dt
import re

from .lib.historyList.getHistoryList import GetHistoryList
from .lib.myNotDisplayException import MyNotDisplayException

class HistoryListView(ListView):
    template_name = 'historyList.html'
    model = HistoryList
    paginate_by = 10
    queryset = HistoryList.objects.order_by('id')

def sync(request):
    print("OK")
    # new_game_data = [["ryu914-sho123-20200319_174123", 1]]
    new_game_data = __getHistoryList()
    if len(new_game_data) == 0:
        # 新規の棋譜が無ければそのまま
        return redirect('add_kifu:historyList')

    history_list_insert = []
    for each_new_game_data in new_game_data:
        # each_new_game_data.append(__get30DaysLater(each_new_game_data[0]))
        history_list_insert.append( HistoryList(game_id=each_new_game_data[0],
                                                my_result=each_new_game_data[1],
                                                save_limit=__get30DaysLater(each_new_game_data[0])) )

    HistoryList.objects.bulk_create(history_list_insert)
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

    # new_game_data = [[id, 勝敗],[...]]
    return new_game_data

def __get30DaysLater(game_id):
    try:
        datetime = re.search('[0-9]{8}_[0-9]{6}', game_id).group()
    except AttributeError as e:
        print(e)
        print("対局日情報が見つかりません")
        return "2099-12-31 23:59:59"
    else:
        datetime_formatted = dt.datetime.strptime(datetime, "%Y%m%d_%H%M%S")
        save_limit = datetime_formatted + dt.timedelta(days=30)
        return make_aware(save_limit.strftime("%Y-%m-%d %H:%M:%S"))

