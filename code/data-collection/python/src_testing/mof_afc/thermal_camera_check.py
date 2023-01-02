from classes_camera import TherCam
from classes_colther import Zaber
from classes_colther import *
from classes_text import *
from saving_data import *

import globals
import time
import threading
import random
import numpy as np

from index_funcs import *

if __name__ == "__main__":
    try:
        zabers = set_up_big_three(globals.axes)

        homingZabersConcu(zabers, globals.haxes)
        globals.positions["camera"]["z"] = 310000
        movetostartZabersConcu(
            zabers, "camera", globals.haxes["colther"], pos=globals.positions["camera"]
        )

        cam = TherCam(30, 34)
        cam.startStream()
        # cam.setShutterManual()
        cam.plotLive()

    except Exception as e:
        errorloc(e)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
