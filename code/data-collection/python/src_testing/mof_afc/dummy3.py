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

        globals.haxes = manualorder(globals.haxes)
        print(globals.haxes)

        colther = set_up_one_zaber("colther", ["x", "y", "z"])
        camera = set_up_one_zaber(
            "camera", ["y", "x", "z"], who="modem", usb_port=2, n_modem=1
        )

        zabers = {"camera": camera["camera"], "colther": colther["colther"]}
        # # Reminder to ask about the age

        homingZabers(zabers, globals.haxes)

        arduino_shutter = ArdUIno(usb_port=2, n_modem=4)
        arduino_shutter.arduino.flushInput()

        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        path_day, path_anal, path_figs, path_data = folderChreation()
        path_videos = folderVhrideos()
        # # name_file = input('Name of the file:  ')
        textes = TextIO()
        textes.subjectN()
        name_subj_file = f"data_subj_{textes.subject_n}"

        data = buildDict("Trial", "Responses")
        main_thread = threading.current_thread()
        # print(main_thread)

        # Recover zaber positions
        globals.positions = csvtoDictZaber(path_data)
        globals.centreROI = csvToDictROI(path_data)

        print(f"Positions Zabers: {globals.positions}")
        print(f"Centre ROI: {globals.centreROI}")

        speaker = initSpeak()
        speech_to_text = initSpeech2Text()
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

        # # Temp file init
        temp_data_writer, temp_file, temp_file_name = tempSaving(path_data)

        response = []

        for i in np.arange(10):
            # cam.performManualff()
            time.sleep(2)
            print(f"Trial number {i}")

            for k, v in reversed(globals.haxes.items()):
                movetostartZabers(
                    zabers, k, list(reversed(v)), pos=globals.positions[k]
                )
                time.sleep(0.1)

            ######### Feedback closure + TONE
            temp = 29.8
            file_path = path_videos + "/" + f"video_subj_{textes.subject_n}_{i}"

            ev = threading.Event()
            beep_trial = threading.Thread(target=beep.play, args=[ev])
            beep_trial.name = "Beep thread"
            beep_trial.start()

            cam.targetTempAuto(file_path, temp, 20, arduino_shutter, ev)

            # ############### Terminate trial
            globals.stimulus = 0
            arduino_shutter.arduino.write(struct.pack(">B", globals.stimulus))
            sa.stop_all()

            time.sleep(0.1)

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

            for t in threading.enumerate():
                print(t.name)

            qs = "Was there any temperature change during the tone?"  # el pavo dice: Was there any temperature change during the tone?
            speak(speaker, qs)

            # print('Global answer')
            # print(globals.answer)
            # print(globals.answered)

            while True:
                if globals.answer == 1:
                    if globals.answered == 1 or globals.answered == 0:
                        print("Answered", globals.answered)
                        break
                    else:
                        globals.answer = 0
                        qs = "I didn't catch that, sorry."  # el pavo dice: Was there any temperature change during the tone?
                        speak(speaker, qs)
                        audio = startAudioWatson()
                        audio_source, q = audioInstance()

                        stream = openStream(audio, q)

                        recognize_yes_no = Thread(
                            target=recognize_yes_no_weboscket,
                            args=[speech_to_text, audio_source, globals.answer],
                        )
                        recognize_yes_no.start()

                        stream.start_stream()

                        qs = "Was there any temperature change during the tone?"  # el pavo dice: Was there any temperature change during the tone?
                        speak(speaker, qs)

            terminateSpeechRecognition(stream, audio, audio_source)

            beep_speech_success.play()

            time.sleep(2)

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
            }

            for k, v in globals.haxes.items():
                movetostartZabers(zabers, k, list(reversed(v)), pos=start_trial_pos[k])
                time.sleep(0.1)

            response.append(globals.answered)
            trial_n = i + 1
            tempRowToWrite = [trial_n, globals.answered]

            # Dictionary saving
            data = appendDataDict(data, tempRowToWrite)
            print(data)

            # Temporal saving
            temp_data_writer.writerow(tempRowToWrite)

            globals.answer = None
            globals.answered = None

        homingZabers(zabers, globals.haxes)

        apendAll(path_data, textes.subject_n, data)
        saveIndv(name_subj_file, path_data, data)

        delTempFiles(path_data)

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)
        temp_file.close()
        changeNameTempFile(path_data)
        terminateSpeechRecognition(stream, audio, audio_source)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        temp_file.close()
        changeNameTempFile(path_data)
        terminateSpeechRecognition(stream, audio, audio_source)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
