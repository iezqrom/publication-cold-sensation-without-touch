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
        subject_n = getSubjNumDec()

        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, subject_n
        )

        # Recover data
        heights = csvtoDictZaber(path_data)
        for i in globals.positions.keys():
            globals.positions[i]["z"] = heights[i]["z"]
        # globals.haxes = manualorder(globals.haxes)
        saveHaxesAll(path_data, globals.haxes)

        print(f"\nPositions Zabers: {globals.positions}\n")
        print(f"\nHaxes: {globals.haxes}")

        zabers = set_up_big_three(globals.axes)
        homingZabersConcu(zabers, globals.haxes)

        arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
        arduino_shutter.arduino.flushInput()

        arduino_dimmer = ArdUIno(usb_port=1, n_modem=24)
        arduino_dimmer.arduino.flushInput()

        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(globals.haxes["colther"])),
            pos=globals.dry_ice_pos,
        )
        os.system("clear")
        input("\n\n Press enter when dry ice is reloaded\n\n")
        homingZabersConcu(zabers, globals.haxes)
        os.system("clear")

        globals.lamp = 1

        try:
            arduino_dimmer.arduino.write(struct.pack(">B", globals.lamp))
        except Exception as e:
            errorloc(e)
            print("DIMMER WRITE FAILED")

        input("\n\n Press enter when lamp time is over\n\n")
        globals.lamp = 0

        try:
            arduino_dimmer.arduino.write(struct.pack(">B", globals.lamp))
        except Exception as e:
            errorloc(e)
            print("DIMMER WRITE FAILED")

        os.system("clear")
        input("\n\n Press enter when participant is comfortable and ready\n\n")

        shakeShutter(arduino_shutter, 5)

        cam.setShutterManual()
        cam.performManualff()
        printme(
            "Performing shutter refresh and taking a 10-second break\nto let the thermal image stabilise"
        )
        time.sleep(10)

        print(f"\nCalculating grids...\n")

        c3 = [3, 6, 9]
        for d in globals.axes.keys():
            globals.grid[d] = grid_calculation(d, 10, pos=globals.positions)
            # print(globals.grid[d].keys())
            for i in globals.grid[d].keys():
                if any(str(pc) == i for pc in c3):
                    if d == "colther":
                        globals.grid[d][i]["z"] += 1920
                    else:
                        globals.grid[d][i]["z"] += 5000
                    # print(globals.grid[d][i]['z'])

            print(globals.grid[d])

        saveGridAll(path_data, globals.grid)

        # moveZabersUp(zabers, ['colther', 'tactile'])
        for k, v in reversed(globals.haxes.items()):
            if k != "tactile":
                movetostartZabersConcu(
                    zabers, k, list(reversed(v)), pos=globals.grid[k]["1"]
                )
            else:
                park_touch = {"x": 0, "y": 0, "z": 209974}
                movetostartZabersConcu(zabers, k, list(reversed(v)), pos=park_touch)

        manual = threading.Thread(
            target=zabers["colther"]["x"].gridCon2,
            args=[
                zabers,
                arduino_shutter,
                "n",
                globals.grid,
                globals.ROIs,
                globals.rules,
                globals.haxes,
            ],
            daemon=True,
        )
        manual.start()

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
