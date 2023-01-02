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

# %%

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
        arduino_shutter.arduino.flushInput()

        zabers = set_up_big_three(globals.axes)
        # print(zabers)
        homingZabersConcu(zabers, globals.haxes)

        shakeShutter(arduino_shutter, 5)

        printme("Check Zaber sets are working")

        zabers["colther"]["x"].manualCon3(zabers, arduino_shutter, "n")

        print(globals.positions)

    except Exception as e:
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))

        errorloc(e)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
