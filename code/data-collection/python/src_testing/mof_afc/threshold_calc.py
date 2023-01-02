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
        path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths(situ)

        rootToUser(path_day, path_anal, path_data, path_figs, path_videos, path_audios)

        # Recover data
        subject_n = txtToVar(path_data, 'temp_subj_n')
        mol_videos_name = f'mol_subj{subject_n}_'

        pattern = f'{mol_videos_name}.*\.hdf5$'

        patternc = re.compile(pattern)
        names = []

        for filename in os.listdir(f'{path_videos}'):
            if patternc.match(filename):
                name, form = filename.split('.')
                names.append(name)
                # print(name)
            else:
                continue

        names.sort(key=natural_keys)
        print(names)

        # Calculate threshold
        last_temp = []

        for i, n in enumerate(names):
            print(n)
            t1 = ReAnRaw(f'{path_videos}/{n}')
            t1.datatoDic()
            t1.extractMeansF(name_coorF = 'diff_coor')
            last_temp.append(t1.means[-1])

        threshold = np.mean(last_temp)
        print(f"\nTHRESHOLD: {threshold}\n")
        time.sleep(1)
        
        saveIndvVar(path_data, threshold, 'temp_threshold')
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)

    except Exception as e:
        errorloc(e)
        changeNameTempFile(path_data)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
        
    except KeyboardInterrupt:
        print('Keyboard Interrupt')
        changeNameTempFile(path_data)
        rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
        