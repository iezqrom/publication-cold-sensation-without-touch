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


ports = grabPorts()
print(ports.ports)

zabers = set_up_big_three()

cam = TherCam()
cam.startStream()

homingZabers(zabers)

arduino_shutter = ArdUIno(usb_port=2, n_modem=4)
arduino_shutter.arduino.flushInput()

manual = threading.Thread(
    target=zabers["colther"][0].manualCon3OneCon,
    args=[zabers, 10000, arduino_shutter],
    daemon=True,
)
manual.start()

cam.plotLiveROINE()
