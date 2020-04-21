from .shogitime import Shogitime

def convert2shogitime(filename):
    shogitime = Shogitime()

    path = "source/kifu/" + filename
    # path = "source/kifu/20200310_141940-ryu914-hiroton777.kifu"

    shogitime.getKifFile(path)
    shogitime.parseText()
    shogitime.setStartDiagram()
    shogitime.setAllMove()

    data = shogitime.export()
    return data