from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from django.utils.timezone import localtime
from .models import HistoryList, LatestSync
from history.models import Information, SmallClass
from kifu_app_project.settings import BASE_DIR

from selenium.common.exceptions import TimeoutException
import datetime as dt
import re

from .lib.historyList.getHistoryList import GetHistoryList
from .lib.operation.makeKifFormat import MakeKifFormat
from .lib.operation.htmlConvert import HtmlConvert
from .lib.operation.scraping import Scraping
from .lib.exception.myNotDisplayException import MyNotDisplayException
from .lib.exception.cantScrapingException import CantScrapingException
from .lib.writeFile import WriteFile

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
    new_game_data = __getHistoryList()
    if len(new_game_data) != 0:
        # 新規データの保存
        history_list_insert = []
        for each_new_game_data in reversed(new_game_data):
            history_list_insert.append( HistoryList(game_id=each_new_game_data[0],
                                                    my_result=each_new_game_data[1],
                                                    save_limit=__get30DaysLater(each_new_game_data[0])) )
        HistoryList.objects.bulk_create(history_list_insert)

    # 最終同期時刻の更新
    LatestSync.objects.update_or_create(
        id = 1,
        defaults = {
            "latest_sync": now
        }
    )

    return redirect('add_kifu:historyList')

def __getHistoryList():
    # DB内の最新のゲームIDの取得
    try:
        last_game_id = HistoryList.objects.order_by("id").last().game_id
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
        datetime_formatted = dt.datetime.strptime(datetime, "%Y%m%d_%H%M%S").astimezone(dt.timezone.utc)
        save_limit = datetime_formatted + dt.timedelta(days=30)
        return save_limit

def save(request):
    mkf = MakeKifFormat()
    id_data = request.GET.getlist("game_id_data")

    for x in id_data:
        history_list_object = get_object_or_404(HistoryList, pk=x)
        game_id = history_list_object.game_id
        try:
            filename, datetime, players, kifu, result = __getKifuData(game_id, ope)
            text_list = mkf.makeTextList(datetime, players, kifu, result)
            # text_list = [対局日時, 先手, 後手, , 1手目, ..., 最終手, , 勝敗結果]
        except CantScrapingException as e:
            print(e)
            print("スクレイピングが出来ませんでした")
            return redirect('add_kifu:historyList')
        save_path = BASE_DIR + env.get_value("KIFU_PATH_FROM_ROOT") + filename
        WriteFile.writeFile(save_path, text_list)

        history_list_object.saved = 1
        history_list_object.save()

        information = Information(
            date = dt.datetime.strptime(datetime + '+0900', "%Y/%m/%d %H:%M:%S%z"),
            sente = players["sente"],
            gote = players["gote"],
            result = (len(kifu)+1) % 2,     # TODO 引き分けに未対応
            my_result = history_list_object.my_result,
            small_class = get_object_or_404(SmallClass, pk=1)       # TODO 小分類が固定値
        )
        information.save()

    return redirect('add_kifu:historyList')

def __getKifuData(game_id, ope):
    url = env.get_value('HISTORY_URL_ROOT', str) + game_id

    text = Scraping(url).scrape()

    hc = HtmlConvert(text)
    kifu = []

    symbol_list = hc.extraction()

    for symbol in symbol_list:
        old_x, old_y, x, y, name, promoted = hc.convert(symbol)
        data = mkf.operate(old_x, old_y, x, y, name, promoted)
        te = mkf.getKifu(data)
        kifu.append(te)

    try:
        hc.setDatetime()
        hc.setPlayers()
        hc.setResultReason()
    except CantScrapingException as e:
        print(e)
        print("スクレイピングが出来ませんでした")
        raise CantScrapingException("スクレイピングが出来ませんでした")

    kifu.append(mkf.getFinalMove(hc.result_reason))

    datetime = mkf.getDatetime(hc.datetime)
    players = mkf.getPlayers(hc.players["sente"], hc.players["s_rank"], hc.players["gote"], hc.players["g_rank"])
    filename = mkf.getFilename(hc.players["sente"], hc.players["gote"], hc.datetime)
    result = mkf.getResult(len(kifu)-1, hc.result, len(kifu)%2)

    return filename, datetime, players, kifu, result