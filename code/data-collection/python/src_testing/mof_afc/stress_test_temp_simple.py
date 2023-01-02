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
from failing import *
from saving_data import *

import globals
import time
import threading
import random
import numpy as np
import simpleaudio as sa
import keyboard

# %%

# homingZabers(zabers, haxes)

# manualorder(haxes)
# %%
if __name__ == "__main__":
    try:
        path_figs, path_data = folderChreation()
        name_file = input("Name of the file:  ")

        ports = grabPorts()
        print(ports.ports)

        arduino_shutter = ArdUIno(usb_port=2, n_modem=4)
        arduino_shutter.arduino.flushInput()

        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        colther = set_up_one_zaber("colther", ["x", "y", "z"])
        camera = set_up_one_zaber(
            "camera", ["y", "x", "z"], who="modem", usb_port=2, n_modem=1
        )

        zabers = {"camera": camera["camera"], "colther": colther["colther"]}
        haxes = {"camera": ["x", "y", "z"], "colther": ["y", "x", "z"]}

        # time.sleep(1)

        homingZabers(zabers, haxes)

        shakeShutter(arduino_shutter, 2)

        print(globals.positions)

        print(haxes)

        for k, v in haxes.items():
            movetostartZabers(zabers, k, v, pos=globals.positions[k])
            time.sleep(0.3)

        globals.light = 2
        arduino_shutter.arduino.write(struct.pack(">B", globals.light))

        manual = threading.Thread(
            target=zabers["colther"]["x"].manualCon2,
            args=[zabers, arduino_shutter, "n"],
            daemon=True,
        )
        manual.start()

        cam.plotLiveROINE()

        globals.light = 3
        arduino_shutter.arduino.write(struct.pack(">B", globals.light))

        print(globals.positions)
        haxes = manualorder(haxes)

        print(haxes)

        homingZabers(zabers, haxes)

        for i in np.arange(10):
            print(f"Trial number {i}")

            for k, v in reversed(haxes.items()):
                movetostartZabers(
                    zabers, k, list(reversed(v)), pos=globals.positions[k]
                )
                time.sleep(0.3)

            # Feedback closure
            temp = 28.5
            file_path = path_data + "/" + f"{name_file}_{i}"
            cam.targetTempAuto(
                output=file_path, target_temp=temp, arduino=arduino_shutter
            )

            globals.stimulus = 0
            arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))

            start_trial_pos = {
                "colther": {
                    "x": globals.positions["colther"]["x"],
                    "y": globals.positions["colther"]["y"] - 90000,
                    "z": globals.positions["colther"]["z"] - 90000,
                },
                "camera": {
                    "x": globals.positions["camera"]["x"],
                    "y": globals.positions["camera"]["y"],
                    "z": globals.positions["camera"]["z"] - 90000,
                },
            }

            for k, v in haxes.items():
                print(v)
                movetostartZabers(zabers, k, list(reversed(v)), pos=start_trial_pos[k])
                time.sleep(0.3)

        homingZabers(zabers, haxes)

    except Exception as e:
        errorloc(e)
        plt.close(1)
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
        homingZabers(zabers, haxes)

    except KeyboardInterrupt:
        print("Keyboard interrupt")
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
        homingZabers(zabers, haxes)
