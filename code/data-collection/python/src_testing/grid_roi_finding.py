##### OWN LIBRARIES
from local_functions import thermalCalibration, arduinos_zabers, closeEnvelope
from index_funcs import mkpaths
from classes_arduino import tryexceptArduino, movePanTilt
from grabPorts import grabPorts
from classes_colther import movetostartZabersConcu, triggered_exception, saveGridIndv
from classes_camera import TherCam
from saving_data import (
    csvToDictGridIndv,
    saveROIAll,
    savePanTiltAll,
    saveGridIndv,
    rootToUser,
    csvToDictPanTiltsAll,
)
import globals
from failing import errorloc

##### EXTERNAL LIBRARIES
import threading
import os

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        situ, day = "ex", None
        subject_n = 1
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )

        value_height_colther = min(globals.lut_distances)

        globals.grid["camera"] = csvToDictGridIndv(path_data, "temp_grid_camera.csv")
        globals.grid["colther"] = csvToDictGridIndv(
            path_data, f"temp_grid_{str(value_height_colther)}_colther.csv"
        )

        try:
            globals.PanTilts = csvToDictPanTiltsAll(path_data)

            print(globals.PanTilts)
            print(globals.PanTilts["1"])
        except Exception as e:
            errorloc(e)

        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()

        cam = TherCam(vminT=globals.vminT, vmaxT=globals.vmaxT)
        cam.startStream()
        cam.setShutterManual()

        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(globals.haxes["colther"])),
            pos=globals.dry_ice_pos,
        )
        os.system("clear")

        thermalCalibration(zabers, arduino_syringe, arduino_dimmer, cam)

        movetostartZabersConcu(zabers, "tactile", ["z", "x"], pos=globals.park_touch)

        movetostartZabersConcu(
            zabers, "camera", ["x", "y"], pos=globals.grid["camera"]["1"]
        )

        movePanTilt(arduino_pantilt, globals.PanTilts["1"])

        movetostartZabersConcu(zabers, "camera", ["z"], pos=globals.grid["camera"]["1"])
        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(globals.haxes["colther"])),
            pos=globals.grid["colther"]["1"],
        )

        manual = threading.Thread(
            target=zabers["colther"]["x"].gridCon3pantiltScaling,
            args=[
                zabers,
                arduino_pantilt,
                platform1,
                arduino_syringe,
                globals.PanTilts,
                globals.grid,
                globals.haxes,
                globals.rules,
            ],
            daemon=True,
        )
        manual.start()

        cam.plotLiveROINEcheck(r=globals.size_ROI)

        globals.stimulus = 7
        tryexceptArduino(arduino_syringe, globals.stimulus)

        globals.grid["camera"] = zabers["colther"]["x"].gridcamera

        print(zabers["colther"]["x"].rois)
        print(zabers["colther"]["x"].PanTilts)

        saveROIAll(path_data, zabers["colther"]["x"].rois)
        savePanTiltAll(path_data, zabers["colther"]["x"].PanTilts)

        saveGridIndv("temp_grid", path_data, globals.grid, "camera")

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

        closeEnvelope(
            zabers, platform1, arduino_syringe, arduino_pantilt, arduino_dimmer
        )

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
