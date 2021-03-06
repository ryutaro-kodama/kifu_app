import datetime as dt

from .piece import *
from ..conversion import NumberConvert as nc
from ..conversion import PieceConvert as pc


class Operation():
    def __init__(self):
        self.piece = {'Fu': [Fu(1, 7, 0),
                             Fu(2, 7, 0),
                             Fu(3, 7, 0),
                             Fu(4, 7, 0),
                             Fu(5, 7, 0),
                             Fu(6, 7, 0),
                             Fu(7, 7, 0),
                             Fu(8, 7, 0),
                             Fu(9, 7, 0),
                             Fu(1, 3, 1),
                             Fu(2, 3, 1),
                             Fu(3, 3, 1),
                             Fu(4, 3, 1),
                             Fu(5, 3, 1),
                             Fu(6, 3, 1),
                             Fu(7, 3, 1),
                             Fu(8, 3, 1),
                             Fu(9, 3, 1)],
                      'Kyo': [Kyo(1, 9, 0),
                              Kyo(9, 9, 0),
                              Kyo(1, 1, 1),
                              Kyo(9, 1, 1)],
                      'Kei': [Kei(2, 9, 0),
                              Kei(8, 9, 0),
                              Kei(2, 1, 1),
                              Kei(8, 1, 1)],
                      'Gin': [Gin(3, 9, 0),
                              Gin(7, 9, 0),
                              Gin(3, 1, 1),
                              Gin(7, 1, 1)],
                      'Kin': [Kin(4, 9, 0),
                              Kin(6, 9, 0),
                              Kin(4, 1, 1),
                              Kin(6, 1, 1)],
                      'Hisya': [Hisya(2, 8, 0),
                                Hisya(8, 2, 1)],
                      'Kaku': [Kaku(8, 8, 0),
                               Kaku(2, 2, 1)],
                      'Ou': [Ou(5, 9, 0),
                             Ou(5, 1, 1)]
                      }
        self.before_dest = (0, 0)

    # @param
    ## old_x, old_y: 動く前の座標
    ## x, y: 動いた後の座標
    ## name: その駒の名前(成った後の駒は、成る前で渡す)
    ## promoted: その駒が移動後に成った状態かどうか
    def operate(self, old_x, old_y, x, y, name, promoted):
        old_x = int(old_x); old_y = int(old_y); x = int(x); y = int(y)

        # "同"の処理
        if self.before_dest == (x, y):
            same = 1
        else:
            same = 0
        self.before_dest = (x, y)

        # "打"の処理
        if (old_x, old_y) == (0, 1) or (old_x, old_y) == (1, 0):
            drop = 1
        else:
            drop = 0

        # 動かす駒の探索
        for piece in self.piece[name]:
            if piece.getPosition() == (old_x, old_y):
                break
        else:
            print('駒がありませんでした')

        # "成"の処理
        # 移動後が成った状態で、移動前は成る前の状態のとき、成ったと解釈
        if promoted == 1 and piece.promotion == 0:
            promotion = 1
            piece.promote()
        # 移動後が成った状態で、移動前も成った状態のとき、既に成っていたと解釈
        elif promoted == 1 and piece.promotion == 1:
            promotion = 2
        else:
            promotion = 0

        # 駒を取る処理
        for piece_type in self.piece:
            for other_piece in self.piece[piece_type]:
                if other_piece.getPosition() == (x, y):
                    if piece.player == 0:
                        other_piece.x, other_piece.y, other_piece.player = 0, 1, 0
                    else:
                        other_piece.x, other_piece.y, other_piece.player = 1, 0, 1
                    other_piece.demote()
                    break
            else:
                continue
            break

        piece.move(x, y)

        return [(old_x, old_y), (x, y), name, same, drop, promotion]

    # @param
    ## data = [(前座標のペア), (後座標のペア), 移動前の駒名, '同'フラグ, '打'フラグ, '成'フラグ]
    def getKifu(self, data):
        # old_position = '(' + str(data[0][0]) + str(data[0][1]) + ')'

        if data[3]:
            new_position = "同　"
        else:
            new_position = nc.number2zenkaku(data[1][0]) + nc.number2kansuji(data[1][1])

        if data[5] == 0:
            name = pc.eigo2koma(data[2])
            promotion = ""
        elif data[5] == 1:
            name = pc.eigo2koma(data[2])
            promotion = "成"
        else:
            name = pc.promote(pc.eigo2koma(data[2]))[0]
            promotion = ""

        if data[4]:
            drop = "打"
            old_position = ''
        else:
            drop = ""
            old_position = '(' + str(data[0][0]) + str(data[0][1]) + ')'

        return new_position + name + drop + promotion + old_position

    # @param
    ## datetime: "YYYY-MM-DD hh:mm:ss"表記の文字列
    def getDatetime(self, datetime):
        datetime_formatted = dt.datetime.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        return datetime_formatted.strftime("%Y/%m/%d %H:%M:%S")

    # @param
    ## sente: 先手の名前    ## s_rank: 先手の段位(半角数字)
    ## gote: 後手の名前     ## g_rank: 後手の段位(半角数字)
    def getPlayers(self, sente, s_rank, gote, g_rank):
        return {"sente": sente + "(" + self.convertRank(s_rank) + ")",
                "gote": gote + "(" + self.convertRank(g_rank) + ")"}

    def convertRank(self, rank):
        rank = int(rank)
        if rank >= 2:
            return nc.number2kansuji(rank) + "段"
        elif rank == 1:
            return "初段"
        else:
            return str(rank*-1) + "級"

    # @param
    ## datetime: "YYYY-MM-DD hh:mm:ss"表記の文字列
    ## sente: 先手の名前    ## gote: 後手の名前
    def getFilename(self, sente, gote, datetime):
        datetime_formatted = dt.datetime.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        datetime_filename = datetime_formatted.strftime("%Y%m%d_%H%M%S")
        return datetime_filename + "-" + sente + "-" + gote + ".kifu"

    # @param
    ## result_reason: 勝敗がついた理由
    def getFinalMove(self, result_reason):
        result_reason_list = ["投了", "詰み", "切れ負け", "反則勝ち", "千日手", "持将棋"]
        try:
            return result_reason_list[result_reason]
        except IndexError as e:
            print(e)
            print("勝敗理由が不明です")

    # @param
    ## count: "最後に駒を動かした手"までの手数
    ## result: 0->勝敗がついた　1->引き分け
    def getResult(self, count, result, winner):
        if result == 0:
            if winner == 0:
                message = '先手の勝ち'
            else:
                message = '後手の勝ち'
        else:
            message = f'引き分け'

        return f"まで{count}手で{message}"

    def makeTextList(self, datetime, players, kifu, result):
        text_list = [f'開始日時：{datetime}',
                     f'先手：{players["sente"]}',
                     f'後手：{players["gote"]}',
                     '']

        for x in range(len(kifu)-1):
            text_list.append(f'{x+1}  {kifu[x]}')

        text_list.append('')
        text_list.append(result)

        return text_list

    def printBoard(self):
        for kind in self.piece:
            for piece in self.piece[kind]:
                print(piece.name + "：" + str(piece.getPosition()))

    def getBoardAsDictionary(self):
        board = {y: {x: None for x in reversed(range(1, 10))} for y in range(1, 10)}
        sente_having = {'歩': 0, '香': 0, '桂': 0, '銀': 0, '金': 0, '飛': 0, '角': 0}
        gote_having = {'歩': 0, '香': 0, '桂': 0, '銀': 0, '金': 0, '飛': 0, '角': 0}

        for piece_type in self.piece:
            for each_piece in self.piece[piece_type]:
                x, y = each_piece.getPosition()
                name = pc.eigo2koma(each_piece.name)
                if (x, y) == (0, 1):
                    sente_having[name] += 1
                elif (x, y) == (1, 0):
                    gote_having[name] += 1
                else:
                    if each_piece.player == 0:
                        board[y][x] = name
                    else:
                        board[y][x] = name + "_"

        return board, sente_having, gote_having

    # 指定した座標の駒を取り除く
    def removePiece(self, x, y):
        for piece_type in self.piece:
            for each_piece in self.piece[piece_type]:
                if each_piece.getPosition() == (x, y):
                    self.piece[piece_type].remove(each_piece)

    def bornPiece(self, x, y, name, promoted, turn):
        if name in self.piece:
            tmp_class = globals()[name]
            self.piece[name].append(tmp_class(x, y, turn))
            if promoted == 1:
                self.piece[name][-1].promote()
        else:
            print("駒の表記が違います")

    def initBoard(self):
        # TODO この初期化を__init__にし、平手の盤面作成(現在の__init__)をメソッド化
        self.piece = {'Fu': [],
                      'Kyo': [],
                      'Kei': [],
                      'Gin': [],
                      'Kin': [],
                      'Hisya': [],
                      'Kaku': [],
                      'Ou': []
                      }

    def setHandicapStart(self, handicap):
        if handicap == "":
            pass
        elif handicap == "香落ち":
            board.removePiece(1, 1)
        elif handicap == "右香落ち":
            board.removePiece(9, 1)
        elif handicap == "角落ち":
            board.removePiece(2, 2)
        elif handicap == "飛車落ち":
            board.removePiece(8, 2)
        elif handicap == "飛香落ち":
            board.removePiece(1, 1)
            board.removePiece(8, 2)
        elif handicap == "二枚落ち":
            board.removePiece(2, 2)
            board.removePiece(8, 2)
        elif handicap == "三枚落ち":
            board.removePiece(1, 1)
            board.removePiece(2, 2)
            board.removePiece(8, 2)
        elif handicap == "四枚落ち":
            board.removePiece(1, 1)
            board.removePiece(9, 1)
            board.removePiece(2, 2)
            board.removePiece(8, 2)
        elif handicap == "五枚落ち":
            board.removePiece(1, 1)
            board.removePiece(2, 1)
            board.removePiece(9, 1)
            board.removePiece(2, 2)
            board.removePiece(8, 2)
        elif handicap == "左五枚落ち":
            board.removePiece(1, 1)
            board.removePiece(8, 1)
            board.removePiece(9, 1)
            board.removePiece(2, 2)
            board.removePiece(8, 2)
        elif handicap == "六枚落ち":
            board.removePiece(1, 1)
            board.removePiece(2, 1)
            board.removePiece(8, 1)
            board.removePiece(9, 1)
            board.removePiece(2, 2)
            board.removePiece(8, 2)
        elif handicap == "八枚落ち":
            board.removePiece(1, 1)
            board.removePiece(2, 1)
            board.removePiece(3, 1)
            board.removePiece(7, 1)
            board.removePiece(8, 1)
            board.removePiece(9, 1)
            board.removePiece(2, 2)
            board.removePiece(8, 2)
        elif handicap == "十枚落ち":
            board.removePiece(1, 1)
            board.removePiece(2, 1)
            board.removePiece(3, 1)
            board.removePiece(4, 1)
            board.removePiece(6, 1)
            board.removePiece(7, 1)
            board.removePiece(8, 1)
            board.removePiece(9, 1)
            board.removePiece(2, 2)
            board.removePiece(8, 2)
        else:
            print("手割合の形式が違います")