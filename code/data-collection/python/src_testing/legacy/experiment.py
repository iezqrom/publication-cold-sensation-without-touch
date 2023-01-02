################################ Import stuff ################################
from classes_thermodes import Thermode
from classes_arduino import ArdUIno
from classes_arduino import *
from classes_colther import Zaber
from classes_camera import TherCam
from saving_data import *
from classes_text import TextIO
from grabPorts import grabPorts
from classes_audio import Sound

import globals
import time
import threading
import random
import numpy as np
import simpleaudio as sa

################################ Defining some useful functions ############################
# To home all zabers
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


################################ Function for Experiment ############################
def experiment(eng):
    ################################ Set constants and objects ################################

    globals.frames["start"][1] = "on"
    print("All ports:")
    ports = grabPorts()
    print(ports.ports)
    ### Camera
    globals.cam = TherCam()
    globals.cam.startStream()

    ### Zabers
    colther1 = Zaber(1, who="serial")
    colther2 = Zaber(2, port=colther1, who="serial")
    colther3 = Zaber(3, port=colther1, who="serial")

    camera12 = Zaber(1, who="modem", usb_port=2, n_modem=1)
    camera1 = camera12.device.axis(1)
    camera2 = camera12.device.axis(2)
    camera3 = Zaber(2, port=camera12, who="modem", usb_port=2, n_modem=1)

    tactile12 = Zaber(1, who="modem", usb_port=2, n_modem=2)
    tactile1 = tactile12.device.axis(1)
    tactile2 = tactile12.device.axis(2)
    tactile3 = Zaber(2, port=tactile12, who="modem", usb_port=2, n_modem=2)

    colther = [colther3, colther2, colther1]
    camera = [camera3, camera2, camera1]
    tactile = [tactile3, tactile2, tactile1]

    zabers = {
        "colther": [colther3, colther2, colther1],
        "camera": [camera3, camera2, camera1],
        "tactile": [tactile3, tactile2, tactile1],
    }

    # Arduino
    arduino_shutter = ArdUIno(usb_port=2, n_modem=4)
    arduino_pressure = ArdUIno(usb_port=1, n_modem=2)

    # Beep
    beep = Sound(400, 10)
    # Homing all the Zabers
    # thread_home_zabers = threading.Thread(target = homingZabers, args = [zabers])
    # thread_shake = threading.Thread(target = shakeShutter, args = [arduino_shutter, 3])
    #
    # thread_home_zabers.start()
    # thread_shake.start()

    # thread_home_zabers.join()
    # thread_shake.join()

    homingZabers(zabers)
    shakeShutter(arduino_shutter, 3)

    # Data
    data = {
        "tactile.experimental": {"rt": [], "temperature": [], "response": [], "RF": []},
        "non_tactile.experimental": {
            "rt": [],
            "temperature": [],
            "response": [],
            "RF": [],
        },
        "tactile.control": {"rt": [], "temperature": [], "response": [], "RF": []},
        "non_tactile.control": {"rt": [], "temperature": [], "response": [], "RF": []},
    }

    n_cond_blocks = 8
    list_trials = globals.conditions * n_cond_blocks
    random.shuffle(list_trials)

    n_boosts = 2
    list_boosts_trials = globals.boost * n_boosts

    trials = list_boosts_trials + list_trials
    random.shuffle(trials)

    n_training = 2
    list_training = globals.conditions * n_training

    n_boosts_training = 1
    list_boosts_training = globals.boost * n_boosts_training

    training = list_boosts_training + list_training
    random.shuffle(training)

    ################################ Setting up ################################
    # Number of participant
    globals.frames["n_participant"][1] = "on"
    globals.frames["start"][1] = "off"

    while globals.frames["n_participant"][1] == "on":
        # print('looping')
        time.sleep(1)

    globals.frames["age"][1] = "on"

    print("Number of participant:  " + str(globals.n_subj))
    # print(type(globals.n_subj))
    #  Ask participant their age

    while globals.frames["age"][1] == "on":
        time.sleep(1)

    print("Age:  " + str(globals.subj_age))

    ################################ FINDING MICROSPOTS ################################
    globals.frames["microspots"][1] = "on"

    while globals.frames["microspots"][1] == "on":
        time.sleep(1)

    # Need to move camera and get readout of skin, we can stay in this screen to monitor temp
    # finish when we are done with finding microspots
    globals.frames["zabering"][1] = "on"

    globals.current_device = "camera"

    thread_zaber_skin_readout = threading.Thread(
        target=camera12.manualConGUIsingle, args=[zabers]
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

    globals.current_device = "camera"

    thread_zabers_big_three = threading.Thread(
        target=camera12.manualConGUIthree, args=[zabers, arduino_shutter]
    )
    thread_zabers_big_three.start()

    while globals.frames["zabering"][1] == "on":
        time.sleep(1)

    globals.hidden = True

    # Printing saved variables
    print("\nPosition Camera: ")
    print(globals.positions["camera"])

    print("Position Colther: ")
    print(globals.positions["colther"])

    print("Position Non-tactile: ")
    print(globals.positions["non_tactile"])

    print("Position Tactile: ")
    print(globals.positions["tactile"])

    print("Centre ROI Control: ")
    print(globals.centreROI["control"])

    print("Centre ROI Experimental: ")
    print(globals.centreROI["experimental"])

    # # ################################ Get height for tactile ##############################
    # Intro
    globals.frames["intro_tactile_height"][1] = "on"

    while globals.frames["intro_tactile_height"][1] == "on":
        time.sleep(1)

    globals.frames["tactile_height"][1] = "on"

    movetostartZabers(zabers, "tactile", "experimental")

    globals.current_device = "tactile"
    # Thread
    e1 = threading.Event()
    e2 = threading.Event()
    es = [e1, e2]

    thread_zaber_skin_readout = threading.Thread(
        target=tactile12.manualConGUIdouble, args=[zabers, es]
    )

    thread_zaber_skin_readout.start()

    arduino_pressure.readFloat(0, -2, globals.pressure, es)

    print("\nPosition Tactile: ")
    print(globals.positions["tactile"])

    ##### Set baseline temperature
    globals.frames["baseline_temp"][1] = "on"
    # print(globals.frames['baseline_temp'][1])

    while globals.frames["baseline_temp"][1] == "on":
        time.sleep(1)

    print("\nBaseline temperature: " + globals.baseline_temp)

    ################################ Experiment #######################################
    ### Training
    globals.frames["intro_training"][1] = "on"

    while globals.frames["intro_training"][1] == "on":
        time.sleep(1)

    # QUEST for training
    # Setting up 1 prior distribution and 4 QUEST algorithms
    alphas = np.arange(28, 32.01, 0.01)
    alphas_list = list(alphas)
    alphas_ll = []
    for i in alphas_list:
        alphas_ll.append(round(i, 2))

    alphas_ll = [float(i) for i in alphas_ll]

    # QUEST algorithms
    TR_tact_exp = eng.quest_matlab_set_up(alphas_ll, nargout=1)
    TR_non_tact_exp = eng.quest_matlab_set_up(alphas_ll, nargout=1)

    TR_tact_con = eng.quest_matlab_set_up(alphas_ll, nargout=1)
    TR_non_tact_con = eng.quest_matlab_set_up(alphas_ll, nargout=1)

    TR_dict = {
        "tactile.experimental": TR_tact_exp,
        "non_tactile.experimental": TR_non_tact_exp,
        "tactile.control": TR_tact_con,
        "non_tactile.control": TR_non_tact_con,
    }

    temp_training = float(globals.baseline_temp) - 2

    while globals.training_boolean == "n":
        for i in np.arange(len(training)):
            train_string = training[i][0] + "." + training[i][1]
            print(training[i][1])
            # Move zabers tactile
            movetostartZabers(zabers, training[i][0], training[i][1])
            # Move zabers camera
            movetostartZabers(zabers, "colther", training[i][1])
            # Move zabers camera
            movetostartZabers(zabers, "camera", training[i][1])

            # Injecting booster
            if len(training[i]) > 2:
                temp_training = 29

            # Open shutter, PID & sound
            globals.frames["fixation_cross"][1] = "on"

            # Set threads
            evPID_train = threading.Event()
            # evBEEP = threading.Event()

            PID_train = threading.Thread(
                target=colther1.ROIPID,
                args=[
                    zabers["colther"],
                    temp_training,
                    evPID_train,
                    20,
                    arduino_shutter,
                ],
                daemon=True,
            )
            beep_train = threading.Thread(target=beep.play, args=[evPID_train])

            # Start threads
            PID_train.start()
            beep_train.start()

            name_file_training = "training_{}_{}_{}_{}".format(
                globals.n_subj, training[i][0], training[i][1], i
            )
            globals.cam.PIDSavePosMeanShuFixROI(
                output="../src_analysis/thermal_image/test1_14012020/{}".format(
                    name_file_training
                ),
                r=20.0,
                cond=training[i][1],
                duration=10,
                event1=evPID_train,
            )

            sa.stop_all()

            # We get response and RT from participant
            globals.frames["response"][1] = "on"
            globals.frames["fixation_cross"][1] = "off"
            start_reply_train = time.time()

            while globals.frames["response"][1] == "on":
                time.sleep(1)

            globals.frames["fixation_cross"][1] = "on"

            end_reply_train = time.time()
            rt_trial_train = end_reply_train - start_reply_train

            if globals.answer == "a":  # YES
                response_train = 1
            elif globals.answer == "s":  # NO
                response_train = 0

            # Get pdf for next trial
            TR_dict[train_string] = eng.quest_matlab_update(
                TR_dict[train_string], temp_training, response_train
            )

            #
            data_training = [
                rt_trial_train,
                temp_training,
                response_train,
                TR_dict[train_string],
            ]
            print("Threshold trial: ")
            print(temp_training)

            temp_training = TR_dict[train_string]["xCurrent"]

            print("Response: " + globals.answer)
            print("Reaction Time: " + str(rt_trial_train))
            homingZabers(zabers)

        globals.frames["fixation_cross"][1] = "off"
        globals.frames["repeat_training"][1] = "on"

        while globals.frames["repeat_training"][1] == "on":
            time.sleep(1)

    ### Trials
    globals.frames["intro_trials"][1] = "on"

    while globals.frames["intro_trials"][1] == "on":
        time.sleep(1)

    # Set up QUEST algorithms
    RF_tact_exp = eng.quest_matlab_set_up(alphas_ll, nargout=1)
    RF_non_tact_exp = eng.quest_matlab_set_up(alphas_ll, nargout=1)

    RF_tact_con = eng.quest_matlab_set_up(alphas_ll, nargout=1)
    RF_non_tact_con = eng.quest_matlab_set_up(alphas_ll, nargout=1)

    RF_dict = {
        "tactile.experimental": RF_tact_exp,
        "non_tactile.experimental": RF_non_tact_exp,
        "tactile.control": RF_tact_con,
        "non_tactile.control": RF_non_tact_con,
    }

    temp_trial = globals.baseline_temp - 2
    # counter = 0

    for i in np.arange(len(trials)):  # RF['stop'] == 0:
        cond_string = trials[i][0] + "." + trials[i][1]
        print()
        # Move Zaber to position
        movetostartZabers(zabers, trials[i][0], trials[i][1])

        # Injecting booster
        if len(trials[i]) > 2:
            temp_trial = 29

        globals.frames["fixation_cross"][1] = "on"

        # Open shutter and PID
        globals.frames["fixation_cross"][1] = "on"

        # Set threads
        evPID = threading.Event()
        # evBEEP = threading.Event()

        PID = threading.Thread(
            target=colther1.ROIPID,
            args=[zabers["colther"], temp_trial, evPID, 20, arduino_shutter],
            daemon=True,
        )
        beep_trial = threading.Thread(target=beep.play, args=[evPID])

        # Start threads
        PID.start()
        beep_trial.start()

        name_file = "{}_{}_{}_{}".format(globals.n_subj, trials[i][0], trials[i][1], i)
        globals.cam.PIDSavePosMeanShuFixROI(
            output="../src_analysis/thermal_image/test1_14012020/{}".format(name_file),
            r=20.0,
            cond=training[i][1],
            duration=10,
            event1=evPID,
        )

        sa.stop_all()

        # We get response and RT from participant
        globals.frames["response"][1] = "on"
        globals.frames["fixation_cross"][1] = "off"
        start_reply = time.time()

        while globals.frames["response"][1] == "on":
            time.sleep(1)

        globals.frames["fixation_cross"][1] = "on"

        end_reply = time.time()
        rt_trial = end_reply - start_reply

        if globals.answer == "a":  # YES
            response_trial = 1
        elif globals.answer == "s":  # NO
            response_trial = 0

        # Get pdf for next trial
        RF_dict[cond_string] = eng.quest_matlab_update(
            RF_dict[cond_string], temp_trial, response_trial
        )

        # Save data to data library
        data_trial = [rt_trial, temp_trial, response_trial, RF_dict[cond_string]]
        llaves_data = data.keys()
        # data[[*llaves_data][0]].keys()
        for (k, v), j in zip(data[cond_string].items(), np.arange(len(data_trial))):
            v.append(data_trial[j])

        temp_trial = RF_dict[cond_string]["xCurrent"]

        print("Response: " + globals.answer)
        print("Reaction Time: " + rt_trial)
        homingZabers(zabers)

        # counter += 1

    # print(data)

    globals.frames["end"][1] = "on"

    ################################ Writing data #####################################
    # Homing all the Zabers
    homingZabers(zabers)

    ### Data
    # Individual file
    saveIndv("nt_vs_t_CS_subj_{}".format(globals.n_subj), globals.n_subj, data)

    # Everyone file
    apendAll("nt_vs_t_CS_ALL", globals.n_subj, data)

    ### AGE
    apendSingle("nt_vs_t_CS_AGE", globals.n_subj, globals.subj_age)

    apendSingle("nt_vs_t_CS_BASELINE_TEMP", globals.n_subj, globals.baseline_temp)
