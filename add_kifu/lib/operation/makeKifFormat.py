from .operation import Operation

class MakeKifFormat(Operation):
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