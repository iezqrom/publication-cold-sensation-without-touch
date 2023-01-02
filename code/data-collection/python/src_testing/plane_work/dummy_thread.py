import globals
import time

import numpy as np


def dummy_thread(eng):

    globals.frames["fixation_cross"][1] = "on"
    print("hola")

    # eng = me.start_matlab()
    alphas = np.arange(28, 32.01, 0.01)

    alphas_list = list(alphas)

    alphas_ll = []
    for i in alphas_list:
        alphas_ll.append(round(i, 2))

    alphas_ll = [float(i) for i in alphas_ll]

    RF = eng.quest_matlab_set_up(alphas_ll, nargout=1)
    # print(RF)

    temp = 30
    counter = 0

    time.sleep(2)

    data = {"rt": [], "temperature": [], "response": [], "grade": [], "RF": []}

    while counter < 5:  # RF['stop'] == 0:

        globals.frames["fixation_cross"][1] = "off"
        start_reply = time.time()
        globals.frames["response"][1] = "on"

        while globals.frames["response"][1] == "on":
            time.sleep(1)

        globals.frames["fixation_cross"][1] = "on"

        end_reply = time.time()

        rt_trial = end_reply - start_reply

        if globals.answer == "y":
            response = 0
        elif globals.answer == "n":
            response = 1

        # print(globals.answer)

        RF = eng.quest_matlab_update(RF, temp, response)

        temp = RF["xCurrent"]
        print(RF["stop"])

        data["RF"].append(RF)
        data["rt"].append(rt_trial)
        data["temperature"].append(temp)
        data["response"].append(response)

        counter += 1

    print(data)

    # while True:
    #     time.sleep(5)
    #     globals.frames_boolean['n_participant'] = 'on'
    #     globals.frames_boolean['start'] = 'off'
    #
    #     while globals.frames_boolean['n_participant'] == 'on':
    #         time.sleep(1)
    #
    #     print(globals.n_subj)
    #
    #     #  Ask participant their age
    #
    #     globals.frames_boolean['age'] = 'on'
    #
    #     while globals.frames_boolean['age'] == 'on':
    #         time.sleep(1)
    #
    #     print(globals.subj_age)
