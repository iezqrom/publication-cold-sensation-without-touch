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

# %%
if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)
        path_day, path_anal, path_figs, path_data = folderChreation()

        zabers = set_up_big_three(globals.axes)
        # # Reminder to ask about the age

        arduino_dis = ArdUIno(usb_port=1, n_modem=21)
        arduino_dis.arduino.flushInput()

        homingZabersConcu(zabers, globals.haxes)

        movetostartZabersConcu(
            zabers, "colther", globals.haxes["colther"], pos=globals.pos_init
        )

        input(
            f"\nPress enter when the participant has finished marking on their sking the laser's positions with the marker pen\n"
        )

        printme("Starting section to find the Z axis position")
        printme("Press 's' to start saving readings from the Ultrasound distance metre")
        printme("Press 'o' to stop saving readings from the Ultrasound distance metre")
        printme("Wait 2 seconds...")

        time.sleep(2)

        # movetostartZabersConcu(zabers, 'colther', globals.haxes['colther'], pos = globals.pos_centre)
        printme("Reading distance metre...")
        arduino_dis.readDistance()

        D = round(np.mean(arduino_dis.buffer), 2)

        printme("D")
        print(D)

        z_ds = {"colther": None, "camera": None, "tactile": None}
        ds = {"colther": 12.24, "camera": 11.55, "tactile": 16.15}
        ds_offset = {"colther": 3, "camera": 0.7, "tactile": 0}

        for i in z_ds:
            z_ds[i] = D - (ds[i] + ds_offset[i])

        print(z_ds)

        for k, v in globals.haxes.items():
            z_steps = z_axis_pos(z_ds[k], globals.step_sizes[k])
            z_ds[k] = z_steps
            globals.positions[k]["z"] = z_ds[k]
            print(f"{k} {z_ds[k]}")

        homingZabersConcu(zabers, globals.haxes)

        # save all z axis positions
        saveZaberPos("temp_zaber_pos", path_data, globals.positions)

    except Exception as e:
        errorloc(e)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
        changeNameTempFile(path_data)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
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
