################################ Import stuff ################################
# %%
from classes_arduino import ArdUIno
from classes_arduino import *
from classes_colther import Zaber
from classes_colther import *
from saving_data import *
from classes_text import TextIO
from classes_text import *
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
from index_funcs import *

# %%
if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)
        situ = parsing_situation()

        if situ == "tb":
            subject_n = numberSubjDay()
        elif situ == "ex":
            subject_n = numberSubjDay("y")

        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, subject_n
        )

        age = agebyExperimenter()

        print(f"\nSubject's number within day: {subject_n}\n")
        print(f"\nSubject's age: {age}\n")

        todaydate, time_now = setSubjNumDec(age, subject_n, situ)

        # Save age and subject number
        apendSingle("age", path_data, subject_n, age)
        saveIndvVar(path_data, subject_n, "temp_subj_n")

        zabers = set_up_big_three(globals.axes)
        # # Reminder to ask about the age

        arduino_dis = ArdUIno(usb_port=1, n_modem=21)
        arduino_dis.arduino.flushInput()

        arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
        arduino_shutter.arduino.flushInput()

        homingZabersConcu(zabers, globals.haxes)

        height_check = False

        subject_n = txtToVar(path_data, "temp_subj_n")

        while not height_check:

            park_touch = {"x": 0, "y": 0, "z": 209974}

            movetostartZabersConcu(
                zabers, "tactile", list(reversed(["x", "y", "z"])), pos=park_touch
            )
            movetostartZabersConcu(
                zabers, "colther", globals.haxes["colther"], pos=globals.pos_init
            )

            input(
                f"\nPress enter when the participant has finished marking on their skin the laser's positions with the marker pen\n"
            )

            printme("Starting section to find the Z axis position")
            printme(
                "Press 's' to start saving readings from the Ultrasound distance metre"
            )
            printme(
                "Press 'o' to stop saving readings from the Ultrasound distance metre"
            )
            printme("Wait 2 seconds...")

            time.sleep(2)

            # movetostartZabersConcu(zabers, 'colther', globals.haxes['colther'], pos = globals.pos_centre)
            printme("Reading distance metre...")
            arduino_dis.readDistance()

            D = round(np.mean(arduino_dis.buffer), 2)

            printme("D")
            print(D)

            z_ds = {"colther": None, "camera": None, "tactile": None}
            # ds = {'colther': 12.32, 'camera': 11.13, 'tactile': 10.87} # before xmas 2020
            # ds = {'colther': 11.40, 'camera': 10.80, 'tactile': 10.5} # 23/03/2021
            ds = {"colther": 11.15, "camera": 10.60, "tactile": 10.30}
            ds_offset = {"colther": 4.3, "camera": 0.6, "tactile": 0}

            for i in z_ds:
                z_ds[i] = D - (ds[i] + ds_offset[i])

            print(z_ds)

            for k, v in globals.haxes.items():
                z_steps = z_axis_pos(z_ds[k], globals.step_sizes[k])
                z_ds[k] = z_steps
                globals.positions[k]["z"] = z_ds[k]
                print(f"{k} {z_ds[k]}")

            #### Home Zabers
            homingZabersConcu(zabers, globals.haxes)

            #### Get grid positions for touch
            globals.grid["tactile"] = grid_calculation(
                "tactile", 10, pos=globals.positions
            )

            ### Move Zaber TOUCH to each position
            for gh in globals.grid_heights.keys():
                # print(globals.grid_heights[gh])
                touch = globals.positions["tactile"]["z"] + globals.grid_heights[gh]

                movetostartZabers(
                    zabers,
                    "tactile",
                    list(globals.haxes["tactile"]),
                    pos=globals.grid["tactile"][gh],
                )

                time.sleep(0.3)
                movetostartZabers(zabers, "tactile", "z", touch)
                printme(f"Grid position {gh}")
                printme("Touching? ASK WHETHER THEY CAN FEEL TOUCH")

                time.sleep(2)

                movetostartZabers(zabers, "tactile", "z", globals.positions["tactile"])
                printme("Untouching...")

            homingZabersConcu(zabers, globals.haxes)
            #### Check whether we are happy with grid positions
            while True:
                ans = input("\nAre we happy with the touch position? (y/n)  ")
                if ans[-1] in ("y", "n"):
                    if ans[-1] == "y":
                        # print(ans)
                        height_check = True
                        break
                    else:

                        break

                else:
                    printme("Only 'y' and 'n' are valid responses")

        homingZabersConcu(zabers, globals.haxes)

        # save all z axis positions
        saveZaberPos("temp_zaber_pos", path_data, globals.positions)
        apendSingle("temp_distance_metre", path_data, subject_n, D)

    except Exception as e:
        errorloc(e)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)
        changeNameTempFile(path_data)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)
        changeNameTempFile(path_data)


# show_instructions = True
# while True:
#     if show_instructions:
#         os.system('clear')
#         printme("Press 'f' to move Colther along the Z axis")
#         printme("Press 'u' to check the distance metre readings")
#         show_instructions = False

#     if keyboard.is_pressed('f'):
#         printme("Controlling Zaber...")
#         zabers['colther']['z'].controlZaxis()
#         show_instructions = True
#         time.sleep(0.5)

#     elif keyboard.is_pressed('u'):
#         printme("Reading distance metre...")
#         arduino_dis.readDistance()
#         show_instructions = True
#         time.sleep(0.5)

#     elif keyboard.is_pressed('e'):
#         break

#     else:
#         show_instructions = False
