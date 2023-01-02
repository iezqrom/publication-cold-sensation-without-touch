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
from classes_conds import *
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

if __name__ == "__main__":

    try:
        ports = grabPorts()
        print(ports.ports)
        path_day, path_anal, path_figs, path_data = folderChreation()
        path_videos = folderVhrideos()

        # Data stuff
        data = buildDict("Subject", "Trial", "Responses", "Touch", "Cold")
        temp_data_writer, temp_file, temp_file_name = tempSaving(
            path_data, list(data.keys())
        )

        zabers = set_up_big_three(globals.axes)
        homingZabersConcu(zabers, globals.haxes)

        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(globals.haxes["colther"])),
            pos=globals.positions["colther"],
        )

        arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
        arduino_shutter.arduino.flushInput()

        cam = TherCam()
        cam.startStream()

        os.system("clear")
        input("\n\n Press enter when dry ice is reloaded\n\n")
        homingZabersConcu(zabers, globals.haxes)

        cam.setShutterManual()
        cam.performManualff()
        printme(
            "Performing shutter refresh and taking a 10-second break\nto let the thermal image stabilise"
        )
        time.sleep(10)

        main_thread = threading.current_thread()
        # print(main_thread)

        # Recover information
        globals.positions = csvtoDictZaber(path_data)
        globals.grid = csvToDictGridAll(path_data)
        globals.haxes = csvToDictHaxes(path_data)
        globals.ROIs = csvToDictROIAll(path_data)
        temp = txtToVar(path_data, "temp_threshold")
        subject_n = txtToVar(path_data, "temp_subj_n")

        name_subj_file = f"data_subj_{int(subject_n)}"
        temp = round(float(temp), 2)
        temp = temp - 0.5

        print(f"\nPositions Zabers: {globals.positions}\n")
        print(f"\nROIs: {globals.ROIs}\n")
        print(f"\nHaxes: {globals.haxes}")
        print(f"\nGrids Colther: {globals.grid['colther']}\n")
        print(f"\nGrids Camera: {globals.grid['camera']}\n")
        print(f"\nGrids Tactile: {globals.grid['tactile']}\n")
        print(f"\nPeak target temperature {temp}\n")

        time.sleep(5)

        speaker = initSpeak()
        speech_to_text = initSpeech2Text()
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

        # # Temp file init

        response = []

        n_trials = 80
        conditions = 2

        stims = sdt_setup(n_trials, conditions)

        init_pos = np.arange(1, 9.01, 1)
        init_rep = np.repeat(init_pos, 3)
        np.random.shuffle(init_rep)

        printme("Randomising grid positions for the next 20 trials...")

        final_order = exp_rand(init_rep, final_order, check_twoD, globals.coor_cells)

        for i, s in enumerate(stims):
            if i % 20 == 0:
                homingZabersConcu(zabers, globals.haxes)

                movetostartZabersConcu(
                    zabers,
                    "colther",
                    list(reversed(globals.haxes["colther"])),
                    pos=globals.positions["colther"],
                )

                os.system("clear")
                input("\n\n Press enter when dry ice is reloaded\n\n")
                homingZabersConcu(zabers, globals.haxes)

                cam.setShutterManual()
                cam.performManualff()
                printme(
                    "Performing shutter refresh and taking a 10-second break\nto let the thermal image stabilise"
                )
                time.sleep(10)

                shakeShutter(arduino_shutter, 5)
                printme("About to resume the experiment")

            p = str(final_order[i])
            cROI = globals.ROIs[p]

            moveZabersUp(devices, ["colther", "tactile"])

            for k, v in reversed(haxes.items()):
                # print(k, v, devices, grid[k][current_roi])
                movetostartZabersConcu(devices, k, list(reversed(v)), pos=grid[k][p])
                time.sleep(0.1)

            print(f"\nTrial number {i + 1}\n")

            ######### Feedback closure + TONE
            file_path = path_videos + "/" + f"sdt_{subject_n}_{i}"

            ev = threading.Event()
            beep_trial = threading.Thread(target=beep.play, args=[ev])
            beep_trial.name = "Beep thread"
            beep_trial.daemon = True
            beep_trial.start()

            if s[1] == 0:
                stimulus = 3
            elif s[1] == 1:
                stimulus = 2

            if s[0] == 1:
                touch = globals.positions["tactile"]["z"] + 10000
                movetostartZabers(zabers, "tactile", "z", pos=touch)

            cam.targetTempAuto(file_path, temp, 20, arduino_shutter, ev, stimulus, cROI)

            # ############### Terminate trial
            sa.stop_all()

            # Initiliase Watson
            audio = startAudioWatson()
            audio_source, q = audioInstance()
            stream = openStream(audio, q)
            recognize_yes_no = Thread(
                target=recognize_yes_no_weboscket,
                args=[speech_to_text, audio_source, globals.answer],
            )
            recognize_yes_no.name = "Speech recognition thread"
            recognize_yes_no.start()

            stream.start_stream()

            qs = "Was there any temperature change during the tone?"  # el pavo dice: Was there any temperature change during the tone?
            speak(speaker, qs)

            while True:
                if globals.answer == 1:
                    if globals.answered == 1 or globals.answered == 0:
                        print("Answered", globals.answered)
                        break

            terminateSpeechRecognition(stream, audio, audio_source)

            beep_speech_success.play()

            response.append(globals.answered)
            trial_n = i + 1
            tempRowToWrite = [subject_n, trial_n, globals.answered, s[0], s[1]]

            # Dictionary saving
            data = appendDataDict(data, tempRowToWrite)
            print(data)

            # Temporal saving
            temp_data_writer.writerow(tempRowToWrite)

            globals.answer = None
            globals.answered = None

        homingZabersConcu(zabers, globals.haxes)

        apendAll(path_data, subject_n, data)
        saveIndv(name_subj_file, path_data, data)

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

        # delTempFiles(path_data)

        for t in threading.enumerate():
            print(t.name)

    except Exception as e:
        errorloc(e)
        temp_file.close()
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

        # changeNameTempFile(path_data)
        terminateSpeechRecognition(stream, audio, audio_source)

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        temp_file.close()
        # changeNameTempFile(path_data)
        terminateSpeechRecognition(stream, audio, audio_source)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
