import numpy as np
import pandas as pd
from classes_audio import Sound
import time
import os

def trial(beep_start, beep_end):
    input("Press Enter to continue...")
    os.system("clear")
    print("ABOUT TO START")
    time.sleep(1)

    beep_start.play()
    time.sleep(2)
    beep_end.play()

    answer = int(input('Answer (0: No // 1: Yes): '))
    return answer

if __name__ == "__main__":
    n_subj = int(input('Subject: '))
    name_file = f'subj{n_subj}_blowing_random'

    file = open(f'../../data/test_blowing/{name_file}.csv', 'w')
    # array with 10 Os and 10 1s
    array_temp = np.concatenate((np.repeat(0, 10), np.repeat(1, 10)))

    # randomise array_temp
    array_temp = np.random.permutation(array_temp)
    array_temp = array_temp.tolist()

    #dictionary with 0 and 1
    dict_temp = {0: [], 1: []}
    message = {0: 'DONT BLOW', 1: 'BLOW'}

    beep_start = Sound(400, 0.3)
    beep_end = Sound(800, 0.3)

    answer = trial(beep_start, beep_end)

    while len(array_temp) > 0:
        # randomly select from array_temp and not replace
        array_temp_rand = array_temp.pop(0)
        print('Condition', message[array_temp_rand])
        answer = trial(beep_start, beep_end)

        dict_temp[array_temp_rand].append(answer)

    #build a pandas dataframe
    df = pd.DataFrame(dict_temp)
    #write to csv
    df.to_csv(file, index=False)

    file.close()
