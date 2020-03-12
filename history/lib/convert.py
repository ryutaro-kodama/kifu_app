class NumberConvert():
    kansuji_list = ['０', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    zenkaku_list = ['０', '１', '２', '３', '４', '５', '６', '７', '８', '９']

    @staticmethod
    def number2kansuji(num):
        return NumberConvert.kansuji_list[num]

    @staticmethod
    def number2zenkaku(num):
        return NumberConvert.zenkaku_list[num]

    @staticmethod
    def kansuji2number(kansuji):
        return NumberConvert.kansuji_list.index(kansuji)

    @staticmethod
    def zenkaku2number(zenkaku):
        return NumberConvert.zenkaku_list.index(zenkaku)

class PieceConvert():
    eigo_koma_list = {'Fu':'歩', 'To':'と',
                      'Kyo':'香', 'NariKyo':'成香',
                      'Kei':'桂', 'NariKei':'成桂',
                      'Gin':'銀', 'NariGin':'成銀',
                      'Kin':'金',
                      'Hisya':'飛', 'Ryu':'竜',
                      'Kaku':'角', 'Uma':'馬',
                      'Ou':'王'}
    nari_list = {'Fu':'To', 'Kyo':'NariKyo', 'Kei':'NariKei', 'Gin':'NariGin', 'HiSya':'Ryu', 'Kaku':'Uma'}

    @staticmethod
    def eigo2koma(eigo):
        return PieceConvert.eigo_koma_list[eigo]

    @staticmethod
    def promote(koma):
        if koma in PieceConvert.nari_list:
            return PieceConvert.nari_list[koma], 1
        else:
            return koma, 0

    @staticmethod
    def demote(koma):
        if koma in PieceConvert.nari_list.values():
            key = [k for k, v in PieceConvert.nari_list.items() if v == koma][0]
            return key, 1
        else:
            return koma, 0