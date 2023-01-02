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
        for d in reversed(vzabers):
            try:
                d.device.send("/set maxspeed 153600")
                d.device.home()
            except:
                d.send("/set maxspeed 153600")
                d.home()


# Move Zabers to starting position
def movetostartZabers(zabers, zaber, cond):
    poses = globals.positions1[zaber]
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


def consPressure():
    zabers["colther"][0].device.send("/set maxspeed 1020000")
    for i in np.arange(5):
        for i in np.arange(2):
            zabers["colther"][0].device.move_rel(80000)
            time.sleep(0.2)
            zabers["colther"][0].device.move_rel(-80000)
            time.sleep(0.2)
        zabers["colther"][0].device.home()
        time.sleep(0.2)
    zabers["colther"][0].device.send("/set maxspeed 153600")


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
            target=zabers["colther"][0].manualCon3OneCon,
            args=[zabers, 10000, arduino_shutter],
            daemon=True,
        )
        manual.start()

        cam.plotLiveROINE()
        beep = Sound(400, 40)

        globals.light = 3
        arduino_shutter.arduino.write(struct.pack(">B", globals.light))

        print(globals.positions1)

        # Define conditions
        cond1 = ["tactile", "non_tactile"]
        trials = ConditionsHandler(cond1)
        trials.repeatition(10)

        # Data structure
        ps = ["rt", "temperature", "trial"]

        data = TestingDataHandler(ps, cond1)

        homingZabers(zabers)

        trial = 1

        for i in np.arange(len(trials.random_repeats)):
            # consPressure()
            movetostartZabers(zabers, "camera", trials.random_repeats[i][0])

            globals.light = 2
            arduino_shutter.arduino.write(struct.pack(">B", globals.light))

            if trials.random_repeats[i][0] == "tactile":
                globals.positions1[trials.random_repeats[i][0]][2] = (
                    globals.positions1[trials.random_repeats[i][0]][2]
                    - globals.amount * 3
                )
                # print(globals.positions1[trials.random_repeats[i][0]][2])
                movetostartZabers(zabers, "tactile", trials.random_repeats[i][0])

            elif trials.random_repeats[i][0] == "non_tactile":
                globals.positions1[trials.random_repeats[i][0]][2] = (
                    globals.positions1[trials.random_repeats[i][0]][2]
                    - globals.amount * 6
                )
                # print(globals.positions1[trials.random_repeats[i][0]][2])
                movetostartZabers(zabers, "non_tactile", trials.random_repeats[i][0])

            movetostartZabers(zabers, "colther", trials.random_repeats[i][0])

            evPID = threading.Event()
            shu = threading.Thread(
                target=arduino_shutter.OpenCloseMoF, args=[evPID], daemon=True
            )
            beep_trial = threading.Thread(target=beep.play, args=[evPID])

            shu.start()
            beep_trial.start()

            if trials.random_repeats[i][0] == "tactile":
                globals.positions1[trials.random_repeats[i][0]][2] = (
                    globals.positions1[trials.random_repeats[i][0]][2]
                    + globals.amount * 3
                )
                movetostartZabers(zabers, "tactile", trials.random_repeats[i][0])

            elif trials.random_repeats[i][0] == "non_tactile":
                globals.positions1[trials.random_repeats[i][0]][2] = (
                    globals.positions1[trials.random_repeats[i][0]][2]
                    + globals.amount * 3
                )
                movetostartZabers(zabers, "non_tactile", trials.random_repeats[i][0])

            cam.refreshShutter()
            time.sleep(0.5)

            evPID.set()

            name_video = "{}_{}_{}_mof".format(
                name_file, trial, trials.random_repeats[i][0]
            )
            folder = "../../src_analysis/test6_17032020/thermal_image"
            cam.rtMoF("{}/{}".format(folder, name_video))

            sa.stop_all()

            globals.light = 3
            arduino_shutter.arduino.write(struct.pack(">B", globals.light))

            homingZabers(zabers)

            trial_data = [globals.rt, globals.thres_temp, trial]

            data.TrialAppend(trial_data, trials.random_repeats[i][0])
            globals.temp = 33

            if trials.random_repeats[i][0] == "non_tactile":
                globals.positions1[trials.random_repeats[i][0]][2] = (
                    globals.positions1[trials.random_repeats[i][0]][2]
                    + globals.amount * 3
                )

            trial += 1

        folder_data = "../../src_analysis/test6_17032020/data"
        saveIndv(name_file, folder_data, data.data)

    except KeyboardInterrupt:
        globals.light = 3
        arduino_shutter.arduino.write(struct.pack(">B", globals.light))

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
        homingZabers(zabers)

        sa.stop_all()
