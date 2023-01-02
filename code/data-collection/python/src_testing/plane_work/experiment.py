################################ Import stuff ################################
from classes_thermodes import Thermode
from classes_arduino import ArdUIno
from classes_colther import Zaber
from classes_camera import TherCam
from saving_data import *
from classes_text import TextIO

import globals
import time
import threading

################################ Defining some useful functions ############################
# To home all zabers
def homingZabers(zabers):
    for kzabers, vzabers in zabers.items():
        for d in vzabers:
            try:
                d.device.home()
            except:
                d.home()


################################ Function for Experiment ############################
def experiment():
    ################################ Set constants and objects ################################

    globals.frames["start"][1] = "on"
    ### Camera object and start streaming
    globals.cam = TherCam()
    globals.cam.startStream()

    ### Zabers' objects
    colther1 = Zaber(1, who="serial")
    colther2 = Zaber(2, port=colther1, who="serial")
    colther3 = Zaber(3, port=colther1, who="serial")

    camera12 = Zaber(1, who="modem", n_modem=1)
    camera1 = camera12.device.axis(1)
    camera2 = camera12.device.axis(2)
    camera3 = Zaber(2, port=camera12, who="modem", n_modem=1)

    tactile12 = Zaber(1, who="modem", n_modem=2)
    tactile1 = tactile12.device.axis(1)
    tactile2 = tactile12.device.axis(2)
    tactile3 = Zaber(2, port=tactile12, who="modem", n_modem=2)

    colther = [colther3, colther2, colther1]
    camera = [camera3, camera2, camera1]
    tactile = [tactile3, tactile2, tactile1]

    zabers = {
        "colther": [colther3, colther2, colther1],
        "camera": [camera3, camera2, camera1],
        "tactile": [tactile3, tactile2, tactile1],
    }

    # Homing all the Zabers
    homingZabers(zabers)

    # Arduino object
    arduino = ArdUIno(n_modem=4)

    # globals.shutter = 'close'
    #
    # arduino.arduino.write(globals.shutter.encode())

    # Data dictionaries
    data = {"rt": [], "temperature": [], "response": [], "grade": [], "RF": []}

    ################################ Setting up ################################
    # Number of participant
    globals.frames["n_participant"][1] = "on"
    globals.frames["start"][1] = "off"

    while globals.frames["n_participant"][1] == "on":
        # print('looping')
        time.sleep(1)

    print("Number of participant:" + str(globals.n_subj))

    #  Ask participant their age

    globals.frames["age"][1] = "on"

    while globals.frames["age"][1] == "on":
        time.sleep(1)

    print("Age:" + str(globals.subj_age))

    ################################ FINDING MICROSPOTS ################################
    globals.frames["microspots"][1] = "on"

    while globals.frames["microspots"][1] == "on":
        time.sleep(1)

    # Need to move camera and get readout of skin, we can stay in this screen to monitor temp
    # finish when we are done with finding microspots
    globals.frames["zabering"][1] = "on"

    thread_zaber_skin_readout = threading.Thread(
        target=camera12.manualConGUIsingle, args=[zabers["camera"]]
    )
    thread_zaber_skin_readout.start()

    while globals.frames["zabering"][1] == "on":
        time.sleep(1)

    ################################ Get position for big three  ########################
    globals.frames["intro_big_three"][1] = "on"

    while globals.frames["intro_big_three"][1] == "on":
        time.sleep(1)

    # Need to move three zabers simultaneously to get colther, tactile and camera well aligned

    globals.hidden = False
    globals.frames["zabering"][1] = "on"

    thread_zabers_big_three = threading.Thread(
        target=camera12.manualConGUIthree, args=[zabers, arduino]
    )
    thread_zabers_big_three.start()

    while globals.frames["zabering"][1] == "on":
        time.sleep(1)

    globals.hidden = True

    # # ################################ Get height for tactile ##############################
    # # # UNFISNISHED
    # globals.frames['tactile_height'][1] = 'on'
    #
    # thread_zaber_skin_readout = threading.Thread(target = tactile12.manualConGUIsingle, args = [zabers['tactile']])
    # thread_zaber_skin_readout.start()
    #
    # while globals.frames['tactile_height'][1] == 'on':
    #     time.sleep(1)
    ###################################################################################
    ################################ Experiment #######################################
    ###################################################################################

    ################################ Training #########################################

    ################################ Trials ###########################################

    ################################ Writing data #####################################
    # Homing all the Zabers

    homingZabers(zabers)
    globals.frames["end"][1] = "on"

    ### SENSITIVITY
    # Individual file
    apendIndv(
        "nt_vs_t_CS_subj_{}".format(globals.n_subj), globals.n_subj, data_sensitivity
    )

    # Everyone file
    apendAll("nt_vs_t_CS_ALL", globals.n_subj, data_sensitivity)

    ### SENSITIVITY
    # Individual file
    # apendIndv('nt_vs_t_CS_subj_{}'.format(globals.n_subj), globals.n_subj, data_detection)

    # Everyone file
    # apendAll('nt_vs_t_CS_ALL', globals.n_subj, data_detection)

    ### AGE
    apendAge("nt_vs_t_CS_AGE", globals.n_subj, globals.subj_age)
