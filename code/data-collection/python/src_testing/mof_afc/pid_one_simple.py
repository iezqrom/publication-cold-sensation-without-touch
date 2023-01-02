# %%
################################ Import stuff ################################
from classes_arduino import ArdUIno
from classes_arduino import *
from classes_colther import Zaber
from classes_colther import *
from classes_camera import TherCam
from saving_data import *
from classes_text import TextIO
from grabPorts import grabPorts
from classes_audio import Sound
from classes_conds import ConditionsHandler
from classes_testData import TestingDataHandler

import globals
import time
import threading
import random
import numpy as np
import simpleaudio as sa
import keyboard

# 1. Get PID working in isolation
##### One Zaber, thermal camera + code,
#####

# 2. Build LUT: some sort of logic.
# If we want to bring the temperature down and the height is too far,
# then we can come closer to the skin. If want to bring temperature up,
# then we can come far or simply close the shutter?

# 3. Then we see how to integrate this with pressing the keys

# 4. Get my own data on how much time does the skin take to recover
# its temperature

# %%

# colther = set_up_one_zaber('colther')
# camera = set_up_one_zaber('camera', who='modem', usb_port = 2, n_modem = 1)

# print(globals.positions)

# time.sleep(1)
# movetostartZabers(zabers, 'camera')
# time.sleep(1)
# movetostartZabers(zabers, 'colther')


# %%
if __name__ == "__main__":
    try:
        name_file = input("Name of the file:  ")
        ports = grabPorts()
        print(ports.ports)

        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        colther = set_up_one_zaber("colther")
        camera = set_up_one_zaber("camera", who="modem", usb_port=2, n_modem=1)

        zabers = {"colther": colther["colther"], "camera": camera["camera"]}

        arduino_shutter = ArdUIno(usb_port=2, n_modem=4)
        arduino_shutter.arduino.flushInput()

        homingZabers(zabers)

        shakeShutter(arduino_shutter, 5)
        print(globals.positions)

        time.sleep(1)
        movetostartZabers(zabers, "camera")
        time.sleep(1)
        movetostartZabers(zabers, "colther")

        manual = threading.Thread(
            target=zabers["colther"][0].manualCon2,
            args=[zabers, arduino_shutter],
            daemon=True,
        )
        manual.start()

        cam.plotLiveROINE()

        print(globals.positions)

        homingZabers(zabers)

        # PID
        temp_training = 26
        time.sleep(1)
        movetostartZabers(zabers, "camera")
        time.sleep(1)
        movetostartZabers(zabers, "colther")

        evPID_train = threading.Event()

        PID_train = threading.Thread(
            target=zabers["colther"][0].ROIPID,
            args=[zabers["colther"], temp_training, evPID_train, arduino_shutter],
            daemon=True,
        )
        PID_train.start()

        cam.PIDROI(
            output="../../src_analysis/data/test8_30092020/{}".format(name_file),
            event1=evPID_train,
        )
        homingZabers(zabers)

    except Exception as e:
        print(e)
        plt.close(1)
        # globals.light = 3
        # arduino_shutter.arduino.write(struct.pack('>B', globals.light))

        homingZabers(zabers)
