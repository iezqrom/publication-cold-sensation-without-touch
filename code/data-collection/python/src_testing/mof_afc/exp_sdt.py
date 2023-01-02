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
from rand_cons import *
import argparse
import wave

from index_funcs import *
import keyboard

if __name__ == "__main__":

    try:
        ports = grabPorts()
        print(ports.ports)
        subject_n = getSubjNumDec()

        situ = parsing_situation()
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, subject_n
        )

        # Data stuff
        data = buildDict(
            "Subject",
            "Trial",
            "Responses",
            "Touch",
            "Cold",
            "Watson_listens",
            "Watson_hypothesises",
            "Watson_confidence",
        )
        temp_data_writer, temp_file, temp_file_name = tempSaving(
            path_data, list(data.keys())
        )

        zabers = set_up_big_three(globals.axes)
        homingZabersConcu(zabers, globals.haxes)

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

        if situ == "ex":
            n_trials = 54 * 2
            # n_trials = 40
            conditions = 2
            stims = sdt_setup(n_trials, conditions)

            init_pos = np.arange(1, 9.01, 1)
            init_rep = np.repeat(init_pos, (6 * 2))
            # init_rep = np.repeat(init_pos, 5)
            np.random.shuffle(init_rep)
<<<<<<< HEAD
            final_order = exp_rand(init_rep, check_twoD, restart = 800, coor_cells=globals.coor_cells)

        elif situ == 'tb':    
=======
            final_order = exp_rand(
                init_rep, check_twoD, restart=800, coor_cells=globals.coor_cells
            )

        elif situ == "tb":
>>>>>>> c50fa6aaa4a7c8b3efbc022296d7c206ab210646
            n_trials = 9
            conditions = 2
            stims = sdt_setup(n_trials, conditions)

            init_pos = np.arange(1, 9.01, 1)
            init_rep = np.repeat(init_pos, 2)
            np.random.shuffle(init_rep)
            final_order = exp_rand(
                init_rep, check_twoD, restart=100, coor_cells=globals.coor_cells
            )

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
        printme("Close shutter")

        os.system("clear")
        input("\n\n Press enter when dry ice is reloaded\n\n")
        homingZabersConcu(zabers, globals.haxes)
        os.system("clear")

        globals.lamp = 1

        try:
            arduino_dimmer.arduino.write(struct.pack(">B", globals.lamp))
        except Exception as e:
            errorloc(e)
            arduino_dimmer = ArdUIno(usb_port=1, n_modem=24)
            arduino_dimmer.arduino.flushInput()
            print("DIMMER WRITE FAILED")

        input("\n\n Press enter when lamp time is over\n\n")
        globals.lamp = 0

        try:
            arduino_dimmer.arduino.write(struct.pack(">B", globals.lamp))
        except Exception as e:
            errorloc(e)
            arduino_dimmer = ArdUIno(usb_port=1, n_modem=24)
            arduino_dimmer.arduino.flushInput()
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

        main_thread = threading.current_thread()
        # print(main_thread)

        # Recover information
        globals.positions = csvtoDictZaber(path_data)
        globals.grid = csvToDictGridAll(path_data)
        globals.haxes = csvToDictHaxes(path_data)
        globals.ROIs = csvToDictROIAll(path_data)
        delta = txtToVar(path_data, "temp_delta")
        subject_n = txtToVar(path_data, "temp_subj_n")

        delta = round(float(delta), 2)
        target_delta = delta + 0.3

        print(f"\nPositions Zabers: {globals.positions}\n")
        print(f"\nROIs: {globals.ROIs}\n")
        print(f"\nHaxes: {globals.haxes}")
        print(f"\nGrids Colther: {globals.grid['colther']}\n")
        print(f"\nGrids Camera: {globals.grid['camera']}\n")
        print(f"\nGrids Tactile: {globals.grid['tactile']}\n")
        print(f"\nPeak delta temperature {target_delta}\n")

        time.sleep(5)

        speaker = initSpeak()
        speech_to_text = initSpeech2Text()
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)
        channels = 1
        fs = 44100

        # # Temp file init

        response = []

        time_sti_pres = []

        globals.stimulus = 4

        for i, s in enumerate(stims):
            if not (i == 0):
                if i % 18 == 0:
                    homingZabersConcu(zabers, globals.haxes)

                    movetostartZabersConcu(
                        zabers,
                        "colther",
                        list(reversed(globals.haxes["colther"])),
                        pos=globals.dry_ice_pos,
                    )

                    globals.stimulus = 0

                    try:
                        arduino_shutter.arduino.write(
                            struct.pack(">B", globals.stimulus)
                        )
                    except Exception as e:
                        errorloc(e)
                        os.system("clear")
                        input("\n\n Press enter when Arduino is fixed...")
                        arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
                        arduino_shutter.arduino.flushInput()

                    printme("Close shutter")

                    os.system("clear")
                    input("\n\n Press enter when dry ice is reloaded\n\n")
                    homingZabersConcu(zabers, globals.haxes)
                    os.system("clear")

                    globals.lamp = 1

                    try:
                        arduino_dimmer.arduino.write(struct.pack(">B", globals.lamp))
                    except Exception as e:
                        errorloc(e)
                        os.system("clear")
                        input("\n\n Press enter when Arduino Dimmer is fixed...")
                        arduino_dimmer = ArdUIno(usb_port=1, n_modem=24)
                        arduino_dimmer.arduino.flushInput()

                    input("\n\n Press enter when lamp time is over\n\n")
                    globals.lamp = 0

                    try:
                        arduino_dimmer.arduino.write(struct.pack(">B", globals.lamp))
                    except Exception as e:
                        errorloc(e)
                        os.system("clear")
                        input("\n\n Press enter when Arduino Dimmer is fixed...")
                        arduino_dimmer = ArdUIno(usb_port=1, n_modem=24)
                        arduino_dimmer.arduino.flushInput()

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

                    try:
                        arduino_shutter.arduino.write(
                            struct.pack(">B", globals.stimulus)
                        )
                    except Exception as e:
                        errorloc(e)
                        arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
                        arduino_shutter.arduino.flushInput()

                    shakeShutter(arduino_shutter, 5)
                    printme("Resuming experiment...")
                    globals.stimulus = 4

            p = str(final_order[i])
            cROI = globals.ROIs[p]
            c1 = [1, 4, 7]
            c2 = [2, 5, 8]
            c3 = [3, 6, 9]

            if final_order[i] == 1:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["1"]
            elif final_order[i] == 2:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["2"]
            elif final_order[i] == 3:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["3"]
            elif final_order[i] == 4:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["4"]
            elif final_order[i] == 5:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["5"]
            elif final_order[i] == 6:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["6"]
            elif final_order[i] == 7:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["7"]
            elif final_order[i] == 8:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["8"]
            elif final_order[i] == 9:
                touch = globals.positions["tactile"]["z"] + globals.grid_heights["9"]

            printme(f"\nTrial number {i + 1}\n")
            printme(f"Grid position {final_order[i]}")
            printme(f"Fixed ROI for this position {cROI}")

            movetostartZabersConcu(
                zabers,
                "camera",
                list(reversed(globals.haxes["camera"])),
                pos=globals.grid["camera"][p],
            )
            movetostartZabers(
                zabers,
                "tactile",
                list(globals.haxes["tactile"]),
                pos=globals.grid["tactile"][p],
            )
            movetostartZabersConcu(
                zabers,
                "colther",
                list(reversed(globals.haxes["colther"])),
                pos=globals.grid["colther"][p],
            )

            ######### Feedback closure + TONE
            file_path = path_videos + "/" + f"sdt_trial{i +1}_pos{p}"

            ev = threading.Event()
            beep_trial = threading.Thread(target=beep.play, args=[ev])
            beep_trial.name = "Beep thread"
            beep_trial.daemon = True
            beep_trial.start()

            if s[1] == 0:
                stimulus = 3
                if len(time_sti_pres) == 0:
                    time_out = np.random.randint(
                        3, 8, size=1
                    ) + np.random.random_sample(1)
                else:
                    time_out = np.random.choice(time_sti_pres)

            elif s[1] == 1:
                stimulus = 2
                time_out = 12

            ev_touch = None

            if s[0] == 1:
                ev_touch = threading.Event()
<<<<<<< HEAD
=======

>>>>>>> c50fa6aaa4a7c8b3efbc022296d7c206ab210646
                def UpDown():
                    movetostartZabers(zabers, "tactile", "z", touch, ev_touch)
                    printme("Touching...")

                    ev_touch.clear()

                    movetostartZabers(
                        zabers, "tactile", "z", globals.positions["tactile"], ev_touch
                    )
                    printme("Untouching...")

                touch_thread = Thread(target=UpDown)
                touch_thread.name = "Touch thread"
                touch_thread.daemon = True
                touch_thread.start()
            #####

            cam.targetTempAutoDiffDelta(
                file_path,
                target_delta,
                cROI,
                20,
                arduino_shutter,
                stimulus,
                time_out,
                ev,
                ev_touch,
            )

            if s[1] == 1:
                if cam.shutter_open_time:
                    time_sti_pres.append(cam.shutter_open_time)

            globals.delta = 0

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

            start = time.time()
            qs = "Was there any temperature change during the tone?"  # el pavo dice: Was there any temperature change during the tone?
            speak(speaker, qs)

            globals.answer = None
            globals.answered = None

            beep_speech_success.play()
            for t in threading.enumerate():
                printme(t.name)

            end = time.time() - start
            # print(end)

            timer_watson = time.time()

            while True:
                time_out_watson = time.time() - timer_watson
                if time_out_watson > 10:
                    globals.answered = 2
                    break
                elif globals.answer == 1:
                    if (
                        globals.answered == 1
                        or globals.answered == 0
                        or time_out_watson > 10
                    ):
                        print("Answered", globals.answered)
                        break

            terminateSpeechRecognition(stream, audio, audio_source)

            beep_speech_success.play()

            # print(globals.frames)

            response.append(globals.answered)
            trial_n = i + 1
            tempRowToWrite = [
                subject_n,
                trial_n,
                globals.answered,
                s[0],
                s[1],
                globals.listened,
                globals.hypothesis,
                globals.confidence,
            ]

            # Dictionary saving
            data = appendDataDict(data, tempRowToWrite)
            print(data)

            globals.stimulus = 4

            try:
                arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
            except Exception as e:
                errorloc(e)
                os.system("clear")
                input("\n\n Press enter when Arduino is fixed...")
                arduino_shutter = ArdUIno(usb_port=1, n_modem=1)
                arduino_shutter.arduino.flushInput()

            # Temporal saving
            temp_data_writer.writerow(tempRowToWrite)

            audio_file_name = f"{path_audios}/response_sdt_trial{trial_n}_wans{globals.answered}_conf{globals.confidence}.wav"
            wf = wave.open(audio_file_name, "wb")
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(b"".join(globals.frames))
            wf.close()

            globals.frames = []

            for k, v in globals.haxes.items():
                iti_pos = globals.grid[k][p].copy()
                if k == "colther":
                    iti_pos["z"] = 0
                elif k == "tactile":
                    iti_pos["z"] = 240000

                if k != "camera":
                    movetostartZabersConcu(zabers, k, list(reversed(v)), pos=iti_pos)
                    time.sleep(0.1)

            if keyboard.is_pressed("p"):
                os.system("clear")
                input("\n\n Press enter when panic is over...")

        homingZabersConcu(zabers, globals.haxes)

        apendAll(path_data, 1, data)

        name_subj_file = f"data_subj"
        saveIndv(name_subj_file, path_data, data)

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

        changeNameTempFile(path_data, outcome="success")

        path_day_bit = path_day.rsplit("/", 3)[-1]
        saveIndvVar(".", path_day_bit, "temp_folder_name")

        for t in threading.enumerate():
            printme(t.name)

    except Exception as e:
        errorloc(e)
        temp_file.close()
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)
        changeNameTempFile(path_data)
        terminateSpeechRecognition(stream, audio, audio_source)

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        temp_file.close()
        changeNameTempFile(path_data)
        terminateSpeechRecognition(stream, audio, audio_source)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

        globals.stimulus = 0
        arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
