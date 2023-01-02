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

        cam.plotLiveROINE(
            record="y",
            output="../../src_analysis/test9_01102020/data/{}".format(name_file),
        )

        homingZabers(zabers)

    except KeyboardInterrupt:
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
        homingZabers(zabers)

    except Exception as e:
        print(e)
        plt.close(1)
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
        homingZabers(zabers)

    finally:
        print("Finally...")
        time.sleep(0.5)
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
        homingZabers(zabers)
