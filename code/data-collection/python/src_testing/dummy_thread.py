import globals
import time
def dummy_thread():
    while True:
        time.sleep(5)
        globals.frames_boolean['n_participant'] = 'on'
        globals.frames_boolean['start'] = 'off'

        while globals.frames_boolean['n_participant'] == 'on':
            time.sleep(1)

        print(globals.n_subj)

        #  Ask participant their age

        globals.frames_boolean['age'] = 'on'

        while globals.frames_boolean['age'] == 'on':
            time.sleep(1)

        print(globals.subj_age)
