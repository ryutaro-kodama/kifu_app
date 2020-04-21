from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.timezone import localtime
from .models import HistoryList, LatestSync
from history.models import Information, SmallClass

from selenium.common.exceptions import TimeoutException
import datetime as dt

from add_kifu.lib.exception.cantScrapingException import CantScrapingException
from add_kifu.lib.viewModule import get30DaysLater, getHistoryList, saveKifuData
from lib.writeFile import WriteFile

import environ

env = environ.Env(DEBUG=(bool,False))
env.read_env('.env')

class HistoryListView(ListView):
    template_name = 'add_kifu/index.html'
    model = HistoryList
    paginate_by = 10
    queryset = HistoryList.objects.filter(saved=0).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_sync"] = localtime(LatestSync.objects.get_or_create(id=1)[0].latest_sync)
        return context

# 対局履歴一覧から、gameIDをDBへ保存
def sync(request):
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
    old_data = HistoryList.objects.filter(save_limit__lt=now)
    # old_data = HistoryList.objects.filter(save_limit__lt=make_aware(dt.datetime(2020, 5, 1, 23, 59, 59)))     # データ削除確認用
    for each_old_data in old_data:
        each_old_data.delete()

    # new_game_data = [["ryu914-sho123-20200319_174123", 1]]
    new_game_data = getHistoryList()
    if len(new_game_data) != 0:
        # 新規データの保存
        history_list_insert = []
        for each_new_game_data in reversed(new_game_data):
            history_list_insert.append( HistoryList(game_id=each_new_game_data[0],
                                                    my_result=each_new_game_data[1],
                                                    save_limit=get30DaysLater(each_new_game_data[0])) )
        HistoryList.objects.bulk_create(history_list_insert)

    # 最終同期時刻の更新
    LatestSync.objects.update_or_create(
        id = 1,
        defaults = {
            "latest_sync": now
        }
    )

    return redirect('add_kifu:index')

def save(request):
    id_data = request.GET.getlist("game_id_data")

    for x in id_data:
        history_list_object = get_object_or_404(HistoryList, pk=x)
        game_id = history_list_object.game_id
        my_result = history_list_object.my_result
        try:
            saveKifuData(game_id, my_result)
        except CantScrapingException as e:
            print(e)
            print("スクレイピングが出来ませんでした")
            return redirect('add_kifu:index')

        history_list_object.saved = 1
        history_list_object.save()

    return redirect('add_kifu:index')