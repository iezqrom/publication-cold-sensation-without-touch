################################ Import stuff ################################
# %%
from classes_arduino import ArdUIno
from classes_arduino import *
from classes_colther import Zaber
from classes_colther import *
from saving_data import *
from classes_text import TextIO
from classes_text import *
from grabPorts import grabPorts
from classes_audio import Sound
from classes_conds import ConditionsHandler
from classes_testData import TestingDataHandler
from classes_camera import TherCam

import globals
import time
import threading
import random
import numpy as np
import simpleaudio as sa

# %%
if __name__ == "__main__":
    try:
        path_day, path_anal, path_figs, path_data = folderChreation()
        path_videos = folderVhrideos()

        ports = grabPorts()
        print(ports.ports)

        cam = TherCam(30, 34)
        cam.startStream()

        zabers = set_up_big_three(globals.axes)
        homingZabersConcu(zabers)

        globals.positions = csvtoDictZaber(path_data)

        print(globals.positions)

        for k, v in reversed(globals.haxes.items()):
            if k = 'camera':
                movetostartZabersConcu(zabers, k, list(reversed(v)), pos = globals.positions[k])

        cam.setShutterManual()
        cam.setPathName(f'{path_data}')
        cam.plotLive()

        homingZabersConcu(zabers, globals.haxes)

    except Exception as e:
        errorloc(e)

    except KeyboardInterrupt:
        print('Keyboard Interrupt')

# %%
# globals.haxes['colther']
# %%
