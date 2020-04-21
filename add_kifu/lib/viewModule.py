from add_kifu.models import HistoryList

import re
import datetime as dt


from add_kifu.lib.exception.myNotDisplayException import MyNotDisplayException
from add_kifu.lib.exception.cantScrapingException import CantScrapingException
from add_kifu.lib.getKifFile.htmlConvert import HtmlConvert
from add_kifu.lib.getKifFile.makeKifFormat import MakeKifFormat
from add_kifu.lib.getKifFile.saveKifFile import SaveKifFile
from add_kifu.lib.getKifFile.scraping import Scraping
from add_kifu.lib.historyList.getHistoryList import GetHistoryList

import environ

env = environ.Env(DEBUG=(bool,False))
env.read_env('.env')

def get30DaysLater(game_id):
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

def getHistoryList():
    try:
        # DB内の最新のゲームIDの取得
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


def saveKifuData(game_id, my_result):
    url = env.get_value('HISTORY_URL_ROOT', str) + game_id

    text = Scraping(url).scrape()

    hc = HtmlConvert(text)
    symbol_list = hc.extraction()

    mkf = MakeKifFormat()
    kifu = []

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

    skf = SaveKifFile(filename, datetime, players["sente"], players["gote"], kifu, result)
    skf.makeKifFile()
    skf.insertInformationTable(my_result)