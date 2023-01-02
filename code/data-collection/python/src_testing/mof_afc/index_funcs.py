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

import argparse


def mkpaths(situ, numdaysubj):
    if situ == "tb":
        path_day, path_data, path_figs, path_datalocal = folderChreation(numdaysubj)
        path_videos = folderVhrideos(numdaysubj)
        path_audio = folderArudio(numdaysubj)
    elif situ == "ex":
        path_day, path_data, path_figs, path_datalocal = folderChreation(
            numdaysubj, "y"
        )
        path_videos = folderVhrideos(numdaysubj, "y")
        path_audio = folderArudio(numdaysubj, "y")

    return path_day, path_data, path_figs, path_datalocal, path_videos, path_audio


def parsing_situation():
    parser = argparse.ArgumentParser(
        description="Experimental situation: troubleshooting (tb) or experimenting (ex)"
    )
    parser.add_argument("-s", type=str)
    args = parser.parse_args()
    situ = args.s

    return situ
