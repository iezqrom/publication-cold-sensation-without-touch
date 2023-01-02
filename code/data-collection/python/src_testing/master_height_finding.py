################################ Import stuff ################################
from grabPorts import grabPorts
import globals
from classes_colther import (
    movetostartZabersConcu,
    triggered_exception,
    grid_calculation,
    homingZabersConcu,
    reducegrid,
)
from saving_data import (
    rootToUser,
    saveIndvVar,
    apendSingle,
    setSubjNumDec,
    saveGridIndv,
)
from classes_text import agebyExperimenter, printme
from failing import pusherWarning, spaceLeftWarning
from index_funcs import mkpaths
from local_functions import (
    closeEnvelope,
    arduinos_zabers,
)

import os

if __name__ == "__main__":
    try:
        ports = grabPorts()
        print(ports.ports)

        pusherWarning(n_pushes=3000)
        spaceLeftWarning()

        situ, day = "ex", None
        subject_n = 1

        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, numdaysubj=subject_n, folder_name=day
        )
        path_day_bit = path_day.rsplit("/", 3)[-1]

        if os.path.exists(f"./src_testing/temp_folder_name.txt"):
            os.remove(f"./src_testing/temp_folder_name.txt")

        saveIndvVar("./src_testing", path_day_bit, "temp_folder_name")

        if situ == "tb":
            age = 1
        elif situ == "ex":
            age = agebyExperimenter()

        print(f"\nSubject's number within day: {subject_n}\n")
        print(f"\nSubject's age: {age}\n")

        todaydate, time_now = setSubjNumDec(age, subject_n, situ)

        ### ARDUINOS & ZABERS
        (
            zabers,
            platform1,
            arduino_pantilt,
            arduino_syringe,
            arduino_dimmer,
        ) = arduinos_zabers()

        # Save age and subject number
        apendSingle("age", path_data, subject_n, age)
        saveIndvVar(path_data, subject_n, "temp_subj_n")

        #### MOVE TO FIRST POINT: DEFAULT POSITION
        movetostartZabersConcu(
            zabers,
            "colther",
            list(reversed(globals.haxes["colther"])),
            pos=globals.dry_ice_pos,
        )

        globals.grid["tactile"] = grid_calculation("tactile", 10, pos=globals.positions)

        globals.grid["tactile"] = reducegrid(
            globals.grid["tactile"], [f"{x}" for x in range(1, 10) if x % 2 == 0]
        )

        movetostartZabersConcu(
            zabers,
            "tactile",
            globals.haxes["tactile"],
            pos=globals.grid["tactile"]["1"],
        )

        print(globals.grid["tactile"])

        zabers["colther"]["x"].gridUpDown(zabers, "tactile")

        globals.grid = zabers["colther"]["x"].gridZs
        homingZabersConcu(zabers, globals.haxes)

        # save all z axis positions
        saveGridIndv("temp_grid", path_data, globals.grid, "tactile")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

        #### HOMER ARDUINOS & ZABERS
        closeEnvelope(
            zabers, platform1, arduino_syringe, arduino_pantilt, arduino_dimmer
        )

    except Exception as e:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_pantilt=arduino_pantilt,
            arduino_dimmer=arduino_dimmer,
            e=e,
        )

    except KeyboardInterrupt:
        triggered_exception(
            zabers=zabers,
            platform=platform1,
            arduino_syringe=arduino_syringe,
            arduino_pantilt=arduino_pantilt,
            arduino_dimmer=arduino_dimmer,
        )
