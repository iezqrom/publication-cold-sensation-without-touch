################################ Import stuff ################################
# %%
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
from classes_conds import *
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
from rand_cons import *
import argparse

from index_funcs import *

# %%

if __name__ == "__main__":
    arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
    arduino_shutter.arduino.flushInput()
    time.sleep(1)

    while True:
        a = input("INPUT:   ")
        arduino_shutter.arduino.write(struct.pack(">B", int(a)))
        time.sleep(1)
