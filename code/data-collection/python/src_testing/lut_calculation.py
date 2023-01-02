##### OWN LIBRARIES
from local_functions import (
    thermalCalibration,
    arduinos_zabers,
    panicButton,
    homeArduinos,
    iti_zaber_dance_in,
    iti_zaber_dance_away,
    trigger_handle_reload,
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
    csvToDictGridIndv,
    csvToDictROIAll,
    csvToDictPanTiltsAll,
    txtToVar,
    rootToUser,
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

        # STIMULATION
        stimulus = 2
        time_out = 10

        thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)
        movetostartZabersConcu(zabers, "tactile", ["z", "x"], pos=globals.park_touch)

        ### AUDIO
        speaker = initSpeak()
        beep_speech_success = Sound(1000, 0.2)
        beep = Sound(400, 40)

        # Recover information
        globals.grid["camera"] = csvToDictGridIndv(path_data, "temp_grid_camera.csv")
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

        n_block = 0
        within_block_counter = 0

        for dist in globals.lut_distances:
            print(dist)
            globals.grid["colther"] = csvToDictGridIndv(
                path_data, f"temp_grid_{dist}_colther.csv"
            )
            movetostartZabersConcu(
                zabers, "tactile", ["z", "x"], pos=globals.park_touch
            )
            for v in globals.grid["colther"].keys():

                globals.stimulus = 6
                tryexceptArduino(arduino_syringe, globals.stimulus)
                globals.stimulus = 4

                # preliminary trial
                p = v
                cROI = globals.ROIs[p]
                printme(f"Grid position: {p}")

                movePanTilt(arduino_pantilt, globals.PanTilts[p])
                iti_zaber_dance_in(zabers, p)

                # Feedback closure + TONE
                file_path = path_videos + "/" + f"lut_distance_{dist}_pos{p}"

                ev = threading.Event()
                beep_trial = threading.Thread(target=beep.play, args=[ev])
                beep_trial.name = "Beep thread"
                beep_trial.daemon = True
                beep_trial.start()

                cam.targetTempAutoDiffDelta(
                    file_path,
                    10,
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
            thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)

        homeArduinos(arduino_syringe, arduino_pantilt, arduino_dimmer)
        homingZabersConcu(zabers, globals.haxes)

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

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
