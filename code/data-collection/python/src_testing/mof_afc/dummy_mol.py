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
from classes_testData import TestingDataHandler
from rand_cons import *

import globals
import time
import threading
import random
import numpy as np
import simpleaudio as sa
import argparse

from index_funcs import *

# %%
if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)
        situ = parsing_situation()
        subject_n = getSubjNumDec()
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, subject_n
        )

        zabers = set_up_big_three(globals.axes)
        homingZabersConcu(zabers, globals.haxes)

        # Recover information
        globals.positions = csvtoDictZaber(path_data)
        globals.grid = csvToDictGridAll(path_data)
        globals.haxes = csvToDictHaxes(path_data)
        globals.ROIs = csvToDictROIAll(path_data)

        print(f"\nPositions Zabers: {globals.positions}\n")
        print(f"\nROIs: {globals.ROIs}\n")
        print(f"\nHaxes: {globals.haxes}")
        print(f"\nGrids Colther: {globals.grid['colther']}\n")
        print(f"\nGrids Camera: {globals.grid['camera']}\n")
        print(f"\nGrids Tactile: {globals.grid['tactile']}\n")

        beep = Sound(400, 40)

        # Arduino
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

        printme("We are about to perform 4 training trials of method of limits")

        ## RANDOMISE POSITIONS
        trials_per_cell = 1
        cells = [1, 3, 7, 9]
        init_rep = np.repeat(cells, trials_per_cell)
        np.random.shuffle(init_rep)

        final_order = exp_rand(init_rep, check_linear, restart=10)

        park_touch = {"x": 0, "y": 0, "z": 209974}
        movetostartZabersConcu(
            zabers, "tactile", list(reversed(["x", "y", "z"])), pos=park_touch
        )

        familiar_stimulation = False

        while not familiar_stimulation:
            # print(familiar_stimulation)
            for i, p in enumerate(final_order):
                if not (i == 0):
                    if i % 20 == 0:
                        homingZabersConcu(zabers, globals.haxes)
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
                            arduino_dimmer.arduino.write(
                                struct.pack(">B", globals.lamp)
                            )
                        except Exception as e:
                            errorloc(e)
                            print("DIMMER WRITE FAILED")

                        input("\n\n Press enter when lamp time is over\n\n")
                        globals.lamp = 0

                        try:
                            arduino_dimmer.arduino.write(
                                struct.pack(">B", globals.lamp)
                            )
                        except Exception as e:
                            errorloc(e)
                            print("DIMMER WRITE FAILED")

                        os.system("clear")
                        input(
                            "\n\n Press enter when participant is comfortable and ready\n\n"
                        )

                        cam.setShutterManual()
                        cam.performManualff()
                        printme(
                            "Performing shutter refresh and taking a 10-second break\nto let the thermal image stabilise"
                        )
                        time.sleep(10)

                        shakeShutter(arduino_shutter, 5)
                        printme("About to resume the experiment")
                        movetostartZabersConcu(
                            zabers,
                            "tactile",
                            list(reversed(["x", "y", "z"])),
                            pos=park_touch,
                        )

                print(f"\nTrial number Training MoL {i + 1}\n")

                moveZabersUp(zabers, ["colther"])

                print(globals.ROIs[str(p)])

                for k, v in reversed(globals.haxes.items()):
                    if k == "tactile":
                        printme("Not moving touch")

                    else:
                        movetostartZabersConcu(
                            zabers, k, list(reversed(v)), pos=globals.grid[k][str(p)]
                        )
                        time.sleep(0.1)

                ev = threading.Event()

                shu = threading.Thread(
                    target=arduino_shutter.OpenCloseMoL, args=[ev], daemon=True
                )
                shu.name = "Shutter thread"

                beep_trial = threading.Thread(
                    target=beep.playEndGlobal, args=[ev], daemon=True
                )
                beep_trial.name = "Beep thread"

                shu.start()
                beep_trial.start()

                name_video = f"training_mol_trial{i+1}_pos{str(p)}"

                cam.rtMoLDiff(f"{path_videos}/{name_video}", ev, globals.ROIs[str(p)])

                globals.temp = 33

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
                    "tactile": {
                        "x": globals.positions["tactile"]["x"],
                        "y": globals.positions["tactile"]["y"] - 90000,
                        "z": globals.positions["tactile"]["z"] - 50000,
                    },
                }

                # MOVE TO NEW GRID POSITION
                for k, v in globals.haxes.items():
                    if k == "tactile":
                        printme("Not moving tactile for mol")
                    else:
                        movetostartZabersConcu(
                            zabers, k, list(reversed(v)), pos=start_trial_pos[k]
                        )
                        time.sleep(0.1)

            homingZabersConcu(zabers, globals.haxes)
            while True:
                ans = input("\nAre we happy with the familiarisation phase? (y/n)  ")
                if ans[-1] in ("y", "n"):
                    if ans[-1] == "y":
                        # print(ans)
                        familiar_stimulation = True
                        break
                    else:
                        break

                else:
                    printme("Only 'y' and 'n' are valid responses")

        # homingZabersConcu(zabers, globals.haxes)
        # rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)
        changeNameTempFile(path_data)

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)
        changeNameTempFile(path_data)

        homingZabersConcu(zabers)
        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))

# %%
