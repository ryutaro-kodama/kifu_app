import re
import json

from lib.operation.operation import Operation
from lib.conversion import PieceConvert as pc
from lib.conversion import NumberConvert as nc

class Shogitime():
    def __init__(self):
        self.sente = ""
        self.gote = ""
        self.handicap = ""
        self.analyzed = False
        self.start_turn = "先手"
        self.board_kif = {"kif":[], "sente_having_str": "", "gote_having_str": ""}
        self.data_kif = []
        self.all_move = [ [ {"手数": 0, "コメント": ""} ] ]

    def getKifFile(self, path):
        with open(path, mode='r', encoding='utf-8') as f:
            text_list = f.readlines()
        self.text_list = [text.strip() for text in text_list]

    def parseText(self):
        for text in self.text_list:
            if text.startswith('#'):
                continue
            elif text.startswith('|'):
                self.board_kif["kif"].append(text)
            elif "先手の持駒" in text or "下手の持駒" in text:
                self.board_kif["sente_having_str"] = re.split('：', text)[1]
            elif "後手の持駒" in text or "上手の持駒" in text:
                self.board_kif["gote_having_str"] = re.split('：', text)[1]
            elif "**Engines" in text:
                self.analyzed = True
            elif "後手番" in text or "上手番" in text:
                self.start_turn = "後手"
            elif '：' in text:
                if "変化：" in text:
                    self.data_kif.append(text)
                    continue
                data = re.split('：', text)[1]
                if "先手" in text or "下手" in text:
                    self.sente = data
                elif "後手" in text or "上手" in text:
                    self.gote = data
                elif "手合割" in text:
                    if data != "平手":
                        self.handicap = data
                        self.start_turn = "後手"
            elif "手数＝" in text:
                # TODO この処理が何のためか不明なので作成できない
                continue
            else:
                self.data_kif.append(text)

    def setEvaluationValue(self):
        if not self.analyzed:
            return
        return

    def setPrediction(self):
        if not self.analyzed:
            return
        return

    def setStartDiagram(self):
        board = Operation()
        if len(self.board_kif["kif"]) != 9:
            board.setHandicapStart(self.handicap)
        else:
            board.initBoard()

            # 盤面の作成
            for y in range(1, 10):
                turn = 0
                x = 10
                dan = self.board_kif["kif"][y-1]

                for i in range(1, len(dan)):
                    if dan[i] == ' ':
                        # ' 'だったら次に来る駒は先手の駒 or 空きマス
                        turn = 0
                        x -= 1
                    elif dan[i] == 'v':
                        # 'v'だったら次に来る駒は後手の駒
                        turn = 1
                        x -= 1
                    elif dan[i] == '|':
                        break
                    elif dan[i] == '・':
                        continue
                    else:
                        name = pc.myFormalize(dan[i])
                        name = pc.koma2eigo(name)
                        name, promoted = pc.demote(name)
                        board.bornPiece(x, y, name, promoted, turn)

            # 持ち駒の追加
            for turn, having_str in enumerate([self.board_kif["sente_having_str"],
                                               self.board_kif["gote_having_str"]]):
                having_list = having_str.split()
                for having in having_list:
                    # ex)having = 歩, having = 銀二
                    if len(having) > 1:
                        # havingが二文字以上なら、同じ駒を複数持っている
                        num = nc.kansuji2number(having[1])
                    else:
                        num = 1

                    for i in range(num):
                        name = pc.koma2eigo(having[0])
                        board.bornPiece(turn, (turn+1)%2, name, 0, turn)

        self.board, self.sente_having, self.gote_having = board.getBoardAsDictionary()
        del board

    def setAllMove(self):
        # self.all_move = [本筋, 1つめの変化, 2つめの変化, ... ,
        #               [0手目(開始局面), 1手目, 2手目, ... ,
        #                   {'手数': , '手番': , '手': , '駒': ,
        #                    '前X': , '前Y': , '後X': , '後Y': ,
        #                    '成り': , 'コメント': }    ]       ]
        num = 0
        branch = 0
        branch_list = []
        # branch_list[i] = 何手目からi+1番目の変化が始まったか
        result_list = []
        # result_list[i] = i番目の変化の勝敗結果
        st_formalize_list = {'成銀': '全', '成桂': '圭', '成香': '杏', '王': '玉', '竜': '龍'}
        # end_list = ['中断', '投了', '持将棋', '千日手', '詰み', '切れ負け', '反則勝ち', '反則負け', '入玉勝ち'];

        for text in self.data_kif:
            text = text.strip()
            # print(self.all_move[branch][-1])

            if text.startswith('*') and num in self.all_move[branch]:
                # '*'で始まり、既に(その変化で)局面が存在する(指された後の)時、コメントを追加
                self.all_move[branch][num]["コメント"] += re.sub(r"^\*", "", text)
            elif re.match(r"\d", text):
                # text = re.sub(r"^\d+ ", "", text).strip()
                # 手数の削除
                num += 1
                move = re.search(r"([１-９同][一二三四五六七八九　])((.打)|(.成\(\d\d\))|(成[銀桂香]\(\d\d\))|(.\(\d\d\)))", text)
                old_position = re.search(r"\(\d\d\)", text)
                turn_str = '▲' if (self.start_turn == '先手' and num % 2 == 1) else '△'

                if move:
                    # 指し手の挿入
                    move = move.group()
                    if move[2] == "成":
                        # 駒名が"成◯"
                        name = st_formalize_list[move[2:4]]
                    elif move[2] in st_formalize_list:
                        # 駒名が"竜"or"王"
                        name = st_formalize_list[move[2]]
                    else:
                        name = move[2]

                    self.all_move[branch].append({
                        '手数': num,
                        '手番': turn_str,
                        '手'  : move,
                        '駒'  : name,
                        '前X' : int(old_position.group()[1]) if old_position else 0,
                        '前Y' : int(old_position.group()[2]) if old_position else 0,
                        '後X' : self.all_move[branch][num-1]["後X"] if '同' in move else nc.zenkaku2number(move[0]),
                        '後Y' : self.all_move[branch][num-1]["後Y"] if '同' in move else nc.kansuji2number(move[1]),
                        '成り': True if re.search(r"([１-９同][一二三四五六七八九　])(.成\(\d\d\))", move) else False,
                        'コメント': '',})
                elif 'パス' in text:
                    self.all_move[branch].append({
                        '手数': num,
                        '手番': turn_str,
                        '手'  : "パス",
                        '駒'  : "",
                        '前Y' : 0,
                        '前X' : 0,
                        '後X' : 0,
                        '後Y' : 0,
                        '成り': False,
                        'コメント': '',})
                else:
                    reason = re.search(r'中断|投了|持将棋|千日手|詰み|切れ負け|反則勝ち|反則負け|入玉勝ち', text).group()
                    result = {'勝者':'', '敗者':'', '理由':reason, '表記':''}
                    # 勝敗の決定
                    if not reason:
                        continue
                    elif reason == "中断":
                        result["表記"] = reason
                    elif reason == "持将棋" or reason == "千日手":
                        result["勝者"] = "引き分け"
                        result["敗者"] = "引き分け"
                        result["表記"] = reason + "で引き分け"
                    elif reason == '投了' or reason == '詰み' or reason == '切れ負け' or reason == '反則負け':
                        result["勝者"] = '△' if turn_str == '▲' else '▲'
                        result["敗者"] = '▲' if turn_str == '▲' else '△'
                        result["表記"] = result["敗者"] + reason + "で" + result["勝者"] + "の勝ち"
                    elif reason == '反則勝ち' or reason == '入玉勝ち':
                        result["勝者"] = '▲' if turn_str == '▲' else '△'
                        result["敗者"] = '△' if turn_str == '▲' else '▲'
                        result["表記"] = result["勝者"] + reason
                    result_list.append(result)
                    continue

            elif text.startswith("変化"):
                tmp = re.search(r"変化：\d+手", text).group()
                num = int(re.search(r"\d+", tmp).group())
                # 分岐が始まる手数(num手目)の取得
                self.all_move.append(self.all_move[0][0:num])
                # 本筋の変化前までの手をコピー
                branch_list.append(num)
                # 変化が始まった手数を記録
                num -= 1
                branch += 1

        self.all_move = {branch: {num: move for num, move in enumerate(branch_data)}
                            for branch, branch_data in enumerate(self.all_move)}
        # 全てをJSONで送れるように辞書化

        for branch, result in enumerate(result_list):
            self.all_move[branch]["勝敗"] = result
            # 各変化の辞書の末尾に勝敗を挿入

        self.all_move["変化手数"] = branch_list

    def export(self):
        data = {"先手名": self.sente, "後手名": self.gote,
                "開始手番": self.start_turn,
                "最終手": "",
                "手合割": self.handicap,
                "評価値": [],
                "読み筋": ["-"],
                "初期局面": {'駒': self.board,
                            "先手の持駒": self.sente_having,
                            "後手の持駒": self.gote_having},
                "全指し手": self.all_move,
                "総手数": len(self.all_move[0])-1,
                "変化": 0}
        return json.dumps(data)