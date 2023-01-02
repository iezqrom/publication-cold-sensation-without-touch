################################ Import stuff ################################
# %%
from classes_arduino import ArdUIno
from classes_arduino import *
from classes_colther import Zaber
from classes_colther import *
from classes_tharnal import *
from classes_camera import TherCam
from saving_data import *
from classes_text import TextIO
from grabPorts import grabPorts
from classes_audio import Sound
from classes_conds import ConditionsHandler
from classes_testData import TestingDataHandler
from classes_tharnal import ReAnRaw

import globals
import time
import threading
import random
import numpy as np
import simpleaudio as sa

from index_funcs import *
import argparse

# %%
if __name__ == "__main__":
    try:
        situ = parsing_situation()
        subject_n = getSubjNumDec()
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(
            situ, subject_n
        )

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

        # Recover data
        subject_n = txtToVar(path_data, "temp_subj_n")
        mol_videos_name = f"mol_"

        pattern = f"{mol_videos_name}.*\.hdf5$"
        patternc = re.compile(pattern)

        names = GrabNamesOrder(patternc, path_videos)

        print(names)

        # Calculate threshold
        deltas = []

        for i, n in enumerate(names):
            print(n)
            dat_im = ReAnRaw(f"{path_videos}/{n}")
            dat_im.datatoDic()

            dat_im.extractMeans()
            dat_im.extractOpenClose("stimulus")
            baseline = np.mean(dat_im.means[: (dat_im.open[0] + 1)])
            # print(dat_im.means)

            dat_im.extractMeans(name_coor="diff_coor")
            # print(dat_im.means)

            threshold = dat_im.means[-1]

            printme(f"Threshold: {threshold}")
            printme(f"Baseline: {baseline}")
            delta_indv = baseline - threshold

            if delta_indv > 0.2 and dat_im.data["time"][-1] < 10:
                printme(f"Delta: {delta_indv}")
                deltas.append(delta_indv)
            else:
                printme("Delta value less than 0.2 OR trial was timed out")

        printme("List of Deltas")
        print(deltas)
        delta = np.mean(deltas)
        printme(f"Mean DELTA: {delta}")
        time.sleep(1)

        saveIndvVar(path_data, delta, "temp_delta")
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)
        changeNameTempFile(path_data)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        changeNameTempFile(path_data)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)
