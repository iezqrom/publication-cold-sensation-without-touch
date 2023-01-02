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


def homingZabers(zabers):
    for kzabers, vzabers in zabers.items():
        for d in vzabers:
            try:
                d.device.home()
            except:
                d.home()


# Move Zabers to starting position
def movetostartZabers(zabers, zaber, cond):
    poses = globals.positions[zaber][cond]
    print("\nMoving Zabers of {} to: ".format(zaber))
    print(poses)

    if zaber == "non_tactile":
        zaber = "tactile"

    for d, p in zip(reversed(zabers[zaber]), poses):
        try:
            d.device.move_abs(p)
            # print(d)
        except:
            d.move_abs(p)


if __name__ == "__main__":
    try:
        name_file = input("Name of the file:  ")

        ports = grabPorts()
        print(ports.ports)

        cam = TherCam()
        cam.startStream()

        ### Zabers
        zabers = set_up_big_three()

        # Arduino
        arduino_shutter = ArdUIno(usb_port=2, n_modem=4)
        arduino_shutter.arduino.flushInput()

        homingZabers(zabers)

        shakeShutter(arduino_shutter, 5)

        globals.light = 2
        arduino_shutter.arduino.write(struct.pack(">B", globals.light))

        manual = threading.Thread(
            target=zabers["colther"][0].manualCon3,
            args=[zabers, 10000, arduino_shutter],
            daemon=True,
        )
        manual.start()

        cam.plotLiveROINE()
        beep = Sound(400, 40)

        globals.light = 3
        arduino_shutter.arduino.write(struct.pack(">B", globals.light))

        print(globals.positions)

        # Define conditions
        cond1 = ["tactile", "non_tactile"]
        cond2 = ["experimental", "control"]
        trials = ConditionsHandler(cond1, cond2)
        trials.repeatition(2)

        # Data structure
        ps = ["rt", "temperature", "trial"]

        data = TestingDataHandler(ps, cond1, cond2)

        homingZabers(zabers)

        trial = 1

        for i in np.arange(len(trials.random_repeats)):
            movetostartZabers(zabers, "camera", trials.random_repeats[i][1])

            if trials.random_repeats[i][0] == "tactile":
                globals.positions[trials.random_repeats[i][0]][
                    trials.random_repeats[i][1]
                ][2] = (
                    globals.positions[trials.random_repeats[i][0]][
                        trials.random_repeats[i][1]
                    ][2]
                    - globals.amount * 3
                )

            elif trials.random_repeats[i][0] == "non_tactile":
                globals.positions[trials.random_repeats[i][0]][
                    trials.random_repeats[i][1]
                ][2] = (
                    globals.positions[trials.random_repeats[i][0]][
                        trials.random_repeats[i][1]
                    ][2]
                    - globals.amount * 6
                )

            movetostartZabers(zabers, "tactile", trials.random_repeats[i][1])

            movetostartZabers(zabers, "colther", trials.random_repeats[i][1])

            evPID = threading.Event()
            shu = threading.Thread(
                target=arduino_shutter.OpenCloseMoF, args=[evPID], daemon=True
            )
            beep_trial = threading.Thread(target=beep.play, args=[evPID])

            shu.start()
            beep_trial.start()

            print(trials.random_repeats[i][0])
            print(trials.random_repeats[i][1])

            if trials.random_repeats[i][0] == "tactile":
                globals.positions[trials.random_repeats[i][0]][
                    trials.random_repeats[i][1]
                ][2] = (
                    globals.positions[trials.random_repeats[i][0]][
                        trials.random_repeats[i][1]
                    ][2]
                    + globals.amount * 3
                )

            elif trials.random_repeats[i][0] == "non_tactile":
                globals.positions[trials.random_repeats[i][0]][
                    trials.random_repeats[i][1]
                ][2] = (
                    globals.positions[trials.random_repeats[i][0]][
                        trials.random_repeats[i][1]
                    ][2]
                    + globals.amount * 3
                )

            movetostartZabers(zabers, "tactile", trials.random_repeats[i][1])

            cam.refreshShutter()
            time.sleep(0.5)

            globals.light = 2
            arduino_shutter.arduino.write(struct.pack(">B", globals.light))
            evPID.set()

            name_video = "{}_{}_{}_{}_mof".format(
                name_file,
                trial,
                trials.random_repeats[i][0],
                trials.random_repeats[i][1],
            )
            folder = "../../src_analysis/test4_13032020/thermal_image"
            cam.rtMoF("{}/{}".format(folder, name_video))

            sa.stop_all()

            homingZabers(zabers)

            trial_data = [globals.rt, globals.thres_temp, trial]

            data.TrialAppend(
                trial_data, trials.random_repeats[i][0], trials.random_repeats[i][1]
            )
            globals.temp = 33
            trial += 1

        folder_data = "../../src_analysis/test4_13032020/data"
        saveIndv(name_file, folder_data, data.data)

    except KeyboardInterrupt:
        globals.light = 3
        arduino_shutter.arduino.write(struct.pack(">B", globals.light))

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
        homingZabers(zabers)

        sa.stop_all()
