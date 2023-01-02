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
from failing import *
from saving_data import *
from classes_speech import *
from classes_audio import Sound
import subprocess
import os
import globals
import time
import threading
import random
import numpy as np
import simpleaudio as sa
import keyboard
import math
from datetime import date
import pyttsx3
import psutil
from index_funcs import *

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)
        situ = parsing_situation()
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ
        )

        # Recover data
        heights = csvtoDictZaber(path_data)
        for i in globals.positions.keys():
            globals.positions[i]["z"] = heights[i]["z"]
        # globals.haxes = manualorder(globals.haxes)
        # saveHaxesAll(path_data, globals.haxes)

        print(f"\nPositions Zabers: {globals.positions}\n")
        print(f"\nHaxes: {globals.haxes}")

        zabers = set_up_big_three(globals.axes)
        homingZabersConcu(zabers, globals.haxes)

        arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
        arduino_shutter.arduino.flushInput()

        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        cam.setShutterManual()
        cam.performManualff()
        printme(
            "Performing shutter refresh and taking a 10-second break\nto let the thermal image stabilise"
        )
        time.sleep(10)

        movetostartZabersConcu(
            zabers, k, list(reversed(v)), pos=globals.positions["camera"]
        )

        cam.plotLiveROINE()

        globals.ROIs = zabers["colther"]["x"].rois

        print(globals.ROIs)

        saveROIAll(path_data, globals.ROIs)

        homingZabersConcu(zabers, globals.haxes)

        # cam.killStreaming()

    except Exception as e:
        errorloc(e)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
        changeNameTempFile(path_data)

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
        changeNameTempFile(path_data)

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
