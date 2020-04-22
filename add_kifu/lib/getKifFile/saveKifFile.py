from django.shortcuts import get_object_or_404
from history.models import Information, SmallClass
from kifu_app_project.settings import BASE_DIR

import datetime as dt

from lib.writeFile import WriteFile as wf

import environ

env = environ.Env(DEBUG=(bool,False))
env.read_env('.env')

# 棋譜形式のテキストを受け取って、ファイル保存とDB情報更新を行う
class SaveKifFile():
    def __init__(self, filename, datetime, sente, gote, kifu, result):
        self.filename = filename
        self.datetime = datetime
        self.sente = sente
        self.gote = gote
        self.kifu = kifu
        self.result = result

    def makeKifFile(self):
        save_path = BASE_DIR + env.get_value("KIFU_PATH_FROM_ROOT") + self.filename

        text_list = [f'開始日時：{self.datetime}',
                     f'先手：{self.sente}',
                     f'後手：{self.gote}',
                     '']

        for index, move in enumerate(self.kifu):
            text_list.append(f'{index+1}  {move}')

        text_list.append('')
        text_list.append(self.result)
        # text_list = [対局日時, 先手, 後手, , 1手目, ..., 最終手, , 勝敗結果]

        wf.writeFile(save_path, text_list)

    def insertInformationTable(self, my_result):
        information = Information(
            filename = self.filename,
            date = dt.datetime.strptime(self.datetime + '+0900', "%Y/%m/%d %H:%M:%S%z"),
            sente = self.sente,
            gote = self.gote,
            result = (len(self.kifu)+1) % 2,     # TODO 引き分けに未対応
            my_result = my_result,
            small_class = get_object_or_404(SmallClass, pk=1)       # TODO 小分類が固定値
        )
        information.save()