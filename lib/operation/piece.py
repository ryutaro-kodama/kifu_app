# 親クラスとして、駒を定義
class Piece():
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.promotion = 0    # 成ったかどうか

    def getPosition(self):
        return (self.x, self.y)

    def move(self, x, y):
        self.x = x
        self.y = y

    # 駒を取られたら、playerフラグを反転
    def captured(self):
        self.player = (self.player + 1) % 2

    def promote(self):
        pass

    def demote(self):
        pass

## 以下、子クラスとして駒の種類を定義
class Fu(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.name = 'Fu'

    def promote(self):
        self.name = 'To'
        self.promotion = 1

    def demote(self):
        self.name = 'Fu'
        self.promotion = 0

class Kyo(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.name = 'Kyo'

    def promote(self):
        self.name = 'NariKyo'
        self.promotion = 1

    def demote(self):
        self.name = 'Kyo'
        self.promotion = 0

class Kei(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.name = 'Kei'

    def promote(self):
        self.name = 'NariKei'
        self.promotion = 1

    def demote(self):
        self.name = 'Kei'
        self.promotion = 0

class Gin(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.name = 'Gin'

    def promote(self):
        self.name = 'NariGin'
        self.promotion = 1

    def demote(self):
        self.name = 'Gin'
        self.promotion = 0

class Kin(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.promotion = -1     # 成らないものは-1
        self.name = 'Kin'

class Hisya(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.name = 'Hisya'

    def promote(self):
        self.name = 'Ryu'
        self.promotion = 1

    def demote(self):
        self.name = 'Hisya'
        self.promotion = 0

class Kaku(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.name = 'Kaku'

    def promote(self):
        self.name = 'Uma'
        self.promotion = 1

    def demote(self):
        self.name = 'Kaku'
        self.promotion = 0

class Ou(Piece):
    def __init__(self, x, y, player):
        super().__init__(x, y, player)
        self.promotion = -1     # 成らないものは-1
        self.name = 'Ou'