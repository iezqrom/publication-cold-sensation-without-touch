##### OWN LIBRARIES
from local_functions import (
    thermalCalibration,
    arduinos_zabers,
    panicButton,
    homeArduinos,
    iti_zaber_dance_in,
    iti_zaber_dance_away,
)
from classes_speech import initSpeak
from index_funcs import mkpaths

from classes_arduino import tryexceptArduino, movePanTilt
from grabPorts import grabPorts
from classes_audio import Sound
from classes_colther import (
    triggered_exception,
    homingZabersConcu,
    movetostartZabersConcu,
)
from classes_camera import TherCam
from saving_data import (
    csvToDictROIAll,
    csvToDictPanTiltsAll,
    txtToVar,
    csvToDictGridIndv,
)
from classes_text import printme
import globals

#### EXTERNAL LIBRARIES
import threading
import simpleaudio as sa
import time

if __name__ == "__main__":
    try:
        # Grab ports
        ports = grabPorts()
        print(ports.ports)
        # Grab subject number
        situ, day = "ex", None
        subject_n = 1

        # Check experimental situation, check and/or create folders
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )

        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()
        #### THERMAL CAMERA
        cam = TherCam()
        cam.startStream()
        cam.setShutterManual()

        thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)
        movetostartZabersConcu(zabers, "tactile", ["z", "x"], pos=globals.park_touch)

        ### AUDIO
        speaker = initSpeak()
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

        value_height_colther = min(globals.lut_distances)

        # Recover information
        globals.grid["camera"] = csvToDictGridIndv(path_data, "temp_grid_camera.csv")
        globals.grid["colther"] = csvToDictGridIndv(
            path_data, f"temp_grid_{str(value_height_colther)}_colther.csv"
        )

        globals.ROIs = csvToDictROIAll(path_data)
        globals.PanTilts = csvToDictPanTiltsAll(path_data)
        subject_n = txtToVar(path_data, "temp_subj_n")

        print(f"\nPositions Zabers: {globals.positions}\n")
        print(f"\nROIs: {globals.ROIs}\n")
        print(f"\nPanTilts: {globals.PanTilts}\n")
        print(f"\nHaxes: {globals.haxes}")
        print(f"\nGrids Colther: {globals.grid['colther']}\n")
        print(f"\nGrids Camera: {globals.grid['camera']}\n")
        print(f"\nGrids Tactile: {globals.grid['tactile']}\n")
        time.sleep(globals.delay_data_display)

        ## RANDOMISE POSITIONS
        cells = [1, 2, 3, 4, 5]
        final_order = [1, 1, 1, 1, 1]
        stimulus = 2
        time_out = globals.time_out_ex

        familiar_stimulation = False
        while not familiar_stimulation:
            for i, p in enumerate(cells):
                globals.stimulus = 6
                tryexceptArduino(arduino_syringe, globals.stimulus)
                globals.stimulus = 4

                # preliminary trial
                p = str(cells[i])
                cROI = globals.ROIs[p]
                printme(f"Grid position: {p}")

                movePanTilt(arduino_pantilt, globals.PanTilts[p])
                iti_zaber_dance_in(zabers, p)

                # Feedback closure + TONE
                file_path = path_videos + "/" + f"training_stair_trial{i+1}_pos{p}"

                ev = threading.Event()
                beep_trial = threading.Thread(target=beep.play, args=[ev])
                beep_trial.name = "Beep thread"
                beep_trial.daemon = True
                beep_trial.start()

                # STIMULATION
                presentabsent = final_order[i]

                cam.targetTempAutoDiffDelta(
                    file_path,
                    globals.initial_staircase_temp,
                    cROI,
                    globals.size_ROI,
                    arduino_syringe,
                    stimulus,
                    time_out,
                    ev,
                )
                globals.delta = 0

                sa.stop_all()

                beep_speech_success.play()
                globals.stimulus = 4
                iti_zaber_dance_away(zabers)

                panicButton()

            homeArduinos(arduino_syringe, arduino_pantilt, arduino_dimmer)
            homingZabersConcu(zabers, globals.haxes)
            familiar_stimulation = True

    except Exception as e:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_dimmer=arduino_dimmer,
            arduino_pantilt=arduino_pantilt,
            e=e,
        )

    except KeyboardInterrupt:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_dimmer=arduino_dimmer,
            arduino_pantilt=arduino_pantilt,
        )
