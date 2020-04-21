from kifu_app_project.settings import BASE_DIR

from .shogitime import Shogitime

import environ

env = environ.Env(DEBUG=(bool,False))
env.read_env('.env')

def convert2shogitime(filename):
    shogitime = Shogitime()

    path = BASE_DIR + env.get_value("KIFU_PATH_FROM_ROOT") + filename
    # path = "source/kifu/20200310_141940-ryu914-hiroton777.kifu"

    shogitime.getKifFile(path)
    shogitime.parseText()
    shogitime.setStartDiagram()
    shogitime.setAllMove()

    data = shogitime.export()
    return data