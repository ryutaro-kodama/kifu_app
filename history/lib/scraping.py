# 対局履歴一覧の抽出
import requests
from bs4 import BeautifulSoup
# import re
# import jaconv
# from . import conversion
# import conversion
# import datetime

class Scraping():
    def __init__(self, url):
        self.url = url

    def scrape(self):
    #棋譜情報のあるHTMLの文字要素（テキスト）化
        html = requests.get(self.url)
        #Requestsを使って、webから取得
        soup = BeautifulSoup(html.text, "html.parser")
        #要素を抽出し、BeautifulSoupオブジェクトを作成
        text = soup.__str__()
        #BeautifulSoupオブジェクトを文字列に変換
        return text

# class Make_KIF(Scraping):
    # player = 'ryu914'
    # winner_dic = {'SENTE':'先手', 'GOTE':'後手', 'DRAW':'引き分け'}
    # win_reason_dic = {'TORYO':'投了', 'CHECKMATE':'詰み', 'DISCONNECT':'接続切れ', 'TIMEOUT':'時間切れ', 'ENTERINGKING':'入玉宣言', 'DRAW_SENNICHI':'千日手', 'OUTE_SENNICHI':'連続王手の千日手による反則負け'}
    # narigoma = {'TO':'FU', 'NY':'KY', 'NK':'KE', 'NG':'GI', 'RY':'HI', 'UM':'KA'}

    # def __init__(self, url):
    #     self.text = self.make_text(url)

    # def extraction(self, target_string_start, target_string_end, text, *limited_text):
    # #text(内のlimited_text)からtarget_string_start~target_string_endを抽出するメソッド
    # #limited_textは可変長で、「○○以降で抽出」の場合、limited_textに○○を入れる
    #     #limited_text_indexを前にズラしていき、これをfindの始点とすることで抽出範囲を絞る
    #     limited_text_index = 0
    #     for x in limited_text:
    #         limited_text_index = text.find(x, limited_text_index)
    #         #limited_text_index以降で、xを探す

    #     start_index = text.find(target_string_start, limited_text_index)
    #     end_index = text.find(target_string_end, start_index+1)
    #     result_string = text[start_index+1:end_index]
    #     return result_string

    # def search_each_dictionary_key(self, dictionary, text, *limited_text):
    # #辞書型リストの各keyから始まる文字列に対して、text内に存在するものを返す
    #     limited_text_index = 0
    #     for x in limited_text:
    #         limited_text_index = text.find(x, limited_text_index)
    #     for key in dictionary.keys():
    #         key_index = text.find(key, limited_text_index)
    #         if key_index>0:
    #         #findは存在しなかったら-1を返すことを考慮
    #             return key

    # def make_game_information(self, text):
    #     game_information_str = self.extraction('"', '"', text, 'var gamedata', 'name:')
    #     game_information = re.split('[-]', game_information_str)

    #     sente_rank = self.extraction('"', '"', text, 'dan0:')
    #     game_information.append(sente_rank)
    #     gote_rank = self.extraction('"', '"', text, 'dan1:')
    #     game_information.append(gote_rank)

    #     filename = f'{game_information[2]}-{game_information[0]}({game_information[3]}) vs {game_information[1]}({game_information[4]}).kif'

    #     date = datetime.datetime.strptime(game_information[2],"%Y%m%d_%H%M%S")
    #     #yyyy-mm-dd hh:mm:ss　型への変換

    #     game_information_dic = {'sente': game_information[0],
    #                             'gote': game_information[1],
    #                             'date': date,
    #                             'sente_rank': game_information[3],
    #                             'gote_rank': game_information[4],
    #                             'filename': filename}

    #     result, my_result = self.judge_result(self.text, game_information_dic)
    #     game_information_dic['result'] = result
    #     game_information_dic['my_result'] = my_result
    #     return game_information_dic
    #     # game_information_dic=[sente:先手の名前, gote:後手の名前, date:対局日時, sente_rank:先手の段位, gote_rank:後手の段位, filename:ファイル名, result:先後の勝敗, my_result:プレイヤーの勝敗]

    # def judge_result(self, text, game_information):
    #     # result=0:先手,1:後手,2:引き分け
    #     # my_result=0:勝ち,1:負け,2:引き分け,3:不参加
    #     winner = self.search_each_dictionary_key(Make_KIF.winner_dic, text, 'receiveMove')

    #     if winner=='SENTE':
    #         result = 0
    #         if game_information['sente']==Make_KIF.player:
    #             my_result = 0
    #         elif game_information['gote']==Make_KIF.player:
    #             my_result = 1
    #         else:
    #             my_result = 3
    #     elif winner=='GOTE':
    #         result = 1
    #         if game_information['sente']==Make_KIF.player:
    #             my_result = 1
    #         elif game_information['gote']==Make_KIF.player:
    #             my_result = 0
    #         else:
    #             my_result = 3
    #     elif winner=='DRAW':
    #         result = 2
    #         if game_information['sente']==Make_KIF.player or game_information['gote']==Make_KIF.player:
    #             my_result = 2
    #         else:
    #             my_result = 3
    #     else:
    #         result = 9
    #         my_result = 9

    #     return result, my_result

    # def convert_game_information(self):
    #     game_information = self.make_game_information(self.text)
    #     self.game_information_KIF['先手'] = f'{game_information["sente"]}({game_information["sente_rank"]})'
    #     self.game_information_KIF['後手'] = f'{game_information["gote"]}({game_information["gote_rank"]})'
    #     self.game_information_KIF['対局日時'] = f'{game_information["date"][:4]}/{game_information["date"][4:6]}/{game_information["date"][6:8]} {game_information["date"][9:11]}:{game_information["date"][11:13]}:{game_information["date"][13:]}'
    #     #self.game_information_KIF=[先手(段位), 後手(段位), 対局日時]


    # def make_kifu(self, text):
    #     kifu = []

    #     kifu_ori = re.findall('[+,-][0-9]{4}[A-Z]{2}', text)
    #     for te in range(len(kifu_ori)):
    #         nari = ''
    #         te_divided = []
    #         te_divided = [kifu_ori[te][:1], kifu_ori[te][1:2], kifu_ori[te][2:3], kifu_ori[te][3:4], kifu_ori[te][4:5], kifu_ori[te][5:]]
    #         # ex) te_divided = [+, 7, 7, 7, 6, FU]
    #         if te_divided[1] == '0' and te_divided[2] == '0':
    #         #持ち駒を打った時
    #             te_divided[3] = jaconv.h2z(te_divided[3], digit=True)
    #             te_divided[4] = conversion.suji2kansuji(te_divided[4])
    #             te_divided[5] = conversion.eigo2koma(te_divided[5])
    #             te_KIF = f'{te_divided[3]}{te_divided[4]}{te_divided[5]}打'
    #         else:
    #         #盤上の駒を動かしたとき
    #             if te > 0:
    #             #2手目以上なら’同’の可能性があり、’成’’不成’の可能性もある
    #                 zente_divided = [kifu_ori[te-1][:1], kifu_ori[te-1][1:2], kifu_ori[te-1][2:3], kifu_ori[te-1][3:4], kifu_ori[te-1][4:5], kifu_ori[te-1][5:]]
    #                 if te_divided[3] == zente_divided[3] and te_divided[4] == zente_divided[4]:
    #                 #前の手と同じ行先なら
    #                     te_divided[3] = '同'
    #                     te_divided[4] = ' '
    #                 else:
    #                     te_divided[3] = jaconv.h2z(te_divided[3], digit=True)
    #                     te_divided[4] = conversion.suji2kansuji(te_divided[4])
    #                 if te_divided[5] in Make_KIF.narigoma:
    #                 #‘成‘の処理
    #                     moto_zahyou = jaconv.h2z(te_divided[1], digit=True) + conversion.suji2kansuji(te_divided[2])
    #                     x = [] #元の座標へ動いた手のリスト
    #                     for i in range(len(kifu)):
    #                         if moto_zahyou in kifu[i]:
    #                             x.append(kifu[i])
    #                             #元の座標へ動いた手を全て加える
    #                             k = i + 1
    #                             while '同' in kifu[k]:
    #                                 x.append(kifu[k])
    #                                 #’同’で動いた手も加える
    #                                 k += 1
    #                     if len(x)==0:
    #                     #元の座標へ動いた手がない場合、初期配置から成り駒になったということなので
    #                         te_divided[5] = Make_KIF.narigoma[te_divided[5]]
    #                         #成る前の駒に戻す
    #                         nari = '成'
    #                     elif '成' in x[-1]:
    #                     #最後に元の座標へ動いた駒が、その手で成ったなら、この手では成ってないので
    #                         pass
    #                     elif conversion.eigo2koma(te_divided[5]) in x[-1]:
    #                     #最後に元の座標へ動いた駒が同じ成り駒なら、既に成っていたということなので
    #                         pass
    #                     else:
    #                     #元の座標へ動いた駒が成り駒でないなら、この手で新しく成ったということなので
    #                         te_divided[5] = Make_KIF.narigoma[te_divided[5]]
    #                         nari = '成'
    #             else:
    #             #1手目は’同’や’成’の可能性はないためそのまま全角に変換
    #                 te_divided[3] = jaconv.h2z(te_divided[3], digit=True)
    #                 te_divided[4] = conversion.suji2kansuji(te_divided[4])
    #             te_divided[5] = conversion.eigo2koma(te_divided[5])
    #             te_KIF = f'{te_divided[3]}{te_divided[4]}{te_divided[5]}{nari}({te_divided[1]}{te_divided[2]})'
    #         kifu.append(te_KIF)

    #     self.append_winner(kifu, text)
    #     #勝敗結果の追加
    #     return kifu

    # def append_winner(self, kifu, text):
    #     winner = self.search_each_dictionary_key(Make_KIF.winner_dic, text, 'receiveMove')
    #     win_reason = self.search_each_dictionary_key(Make_KIF.win_reason_dic, text, 'receiveMove')

    #     te_final = Make_KIF.win_reason_dic[win_reason]
    #     kifu.append(te_final)
    #     if win_reason=='TORYO' or win_reason=='CHECKMATE' or win_reason=='DISCONNECT' or win_reason=='TIMEOUT':
    #         result = f'まで{len(kifu)-1}手で{Make_KIF.winner_dic[winner]}の勝ち'
    #     elif win_reason=='DRAW_SENNICHI':
    #         result = f'まで{len(kifu)-1}手で千日手成立により引き分け'
    #     else:
    #         # 'ENTERINGKING':'入玉宣言', 'DRAW_SENNICHI':'千日手', 'OUTE_SENNICHI':'連続王手の千日手による反則負け'}
    #         result = 'error'
    #     kifu.append(result)

    # def export_KIF(self, text):
    # #KIFファイルとして出力
    #     information = self.make_game_information(text)
    #     kifu = self.make_kifu(text)
    #     date = information['date'].strftime("%Y/%m/%d %H:%M:%S")

    #     f = open(information['filename'], 'a')
    #     f.write('対局日：' + date + '\n')
    #     f.write('\n')
    #     f.write('先手：' + information['sente'] + '(' + information['sente_rank'] + ')' + '\n')
    #     f.write('後手：' + information['gote'] + '(' + information['gote_rank'] + ')' + '\n')
    #     f.write('\n')
    #     for x in range(len(kifu)-1):
    #         te = f'{x+1}  {kifu[x]}'
    #         f.write( te + '\n')
    #     f.write(kifu[x+1] + '\n')
    #     f.close()


# url = "https://shogiwars.heroz.jp/games/ryu914-rugokina-20200215_194851"
# instance = Scraping(url)
# print(instance.scrape())

# url = 'https://kif-pona.heroz.jp/games/maeabcdefgda-ryu914-20191014_173335'
# instance = Make_KIF(url)
# instance.export_KIF(instance.text)
# print(instance.make_game_information(instance.text))
