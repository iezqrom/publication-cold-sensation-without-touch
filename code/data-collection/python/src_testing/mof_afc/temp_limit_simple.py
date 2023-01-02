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

# colther = set_up_one_zaber('colther', ['x', 'y', 'z'])
# camera = set_up_one_zaber('camera', ['y', 'x', 'z'], who='modem', usb_port = 2, n_modem = 1)

# zabers = {'camera': camera['camera'], 'colther': colther['colther']}
# haxes = {'camera': ['z', 'x', 'y'], 'colther': ['x', 'y', 'z']}

# homingZabers(zabers, haxes)

#%%
# zabers = {'camera': camera['camera'], 'colther': colther['colther']}
# haxes = {'camera': ['x', 'y', 'z'], 'colther': ['x', 'y', 'z']}
# haxes = {'camera': ['x', 'y', 'z'], 'colther': ['x', 'y', 'z']}

# movetostartZabers(zabers, 'camera', ['x', 'z', 'y'])


def manualorder(haxes):
    print(f"There are {len(haxes.keys())} set of zabers, their names are: ")
    list_keys = list(haxes.keys())

    for i, k in enumerate(list_keys):
        print(k + " ({})".format(i))

    pos_zabs = tuple(str(i) for i in range(0, len(list_keys)))
    # print(pos_zabs)

    nhaxes = {}
    temp_zabers = []

    for i in np.arange((len(list_keys))):
        temp_axes = []
        # Select the zaber
        if i == 0:
            while True:
                chosen = input("Which Zaber set should we move first?\n")
                if chosen in temp_zabers:
                    print(f"\n{chosen.upper()} has been selected already\n")

                elif chosen in pos_zabs:
                    break
                else:
                    print(f"Only {pos_zabs} are valid answers \n")
                    continue
        else:
            if len(list_keys) > 2:
                while True:
                    chosen = input("Which Zaber set should we move next?   ")
                    if chosen in temp_zabers:
                        print(f"{chosen} has been selected already \n")

                    elif chosen in pos_zabs:
                        break
                    else:
                        print(f"Only {pos_zabs} are valid answers\n")
                        continue
            else:
                set_diff_za = set(list_keys) - set(temp_zabers)
                diff_za = list(set_diff_za)
                chosen = list_keys.index(diff_za[0])
                print(f"\n{list_keys[int(chosen)].upper()} was selected\n")
                # temp_zabers.append(chosen)

        temp_zabers.append(list_keys[int(chosen)])

        # Select 1st the axes
        while True:
            firstaxis = input(
                "Which axis should move first? \n You probably want to choose then one that is above the rest, so they don't crash each other\n"
            )
            if firstaxis in ("x", "y", "z"):
                if firstaxis == "x" and list_keys[int(chosen)] == "colther":
                    print(
                        "It is probably not a good idea to move the x axis of colther first\n "
                    )
                    continue
                else:
                    break
            else:
                print(f"Only 'x', 'y' & 'z' are valid answers\n ")
                continue

        temp_axes.append(firstaxis)
        # Select 2nd the axes
        while True:
            secondaxis = input("Which axis should move next?    ")

            if firstaxis == secondaxis:
                print(f"{secondaxis} has already been selected \n")
                continue

            elif secondaxis in ("x", "y", "z"):
                break

            else:
                print(f"Only 'x', 'y' & 'z' are valid answers \n")
                continue

        temp_axes.append(secondaxis)

        set_diff = set(haxes[list_keys[int(chosen)]]) - set(temp_axes)
        diff = list(set_diff)
        temp_axes.append(diff[0])

        # put into haxes dictionary
        nhaxes[list_keys[int(chosen)]] = temp_axes

    return nhaxes


# %%

# homingZabers(zabers, haxes)

# manualorder(haxes)
# %%
if __name__ == "__main__":
    try:
        name_file = input("Name of the file:  ")
        ports = grabPorts()
        print(ports.ports)

        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        arduino_shutter = ArdUIno(usb_port=2, n_modem=4)
        arduino_shutter.arduino.flushInput()

        colther = set_up_one_zaber("colther", ["x", "y", "z"])
        camera = set_up_one_zaber(
            "camera", ["y", "x", "z"], who="modem", usb_port=2, n_modem=1
        )

        zabers = {"camera": camera["camera"], "colther": colther["colther"]}
        haxes = {"camera": ["x", "y", "z"], "colther": ["y", "x", "z"]}

        shakeShutter(arduino_shutter, 2)

        homingZabers(zabers, haxes)
        print(globals.positions)

        print(haxes)

        for k, v in haxes.items():
            movetostartZabers(zabers, k, v)
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

        for k, v in reversed(haxes.items()):
            movetostartZabers(zabers, k, list(reversed(v)))
            time.sleep(0.3)

        # Feedback closure
        temp = 28.5
        cam.targetTempMan(
            output="../../src_analysis/test13_09102020/data/{}".format(name_file),
            target_temp=temp,
            arduino=arduino_shutter,
        )

        time.sleep(0.1)
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))

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
