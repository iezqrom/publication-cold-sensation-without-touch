import numpy as np 

from saving_data import *
import pandas as pd

class ConditionsHandler():
    
    def __init__(self, *conds):
        self.conditions = np.array(np.meshgrid(*conds)).T.reshape(-1,len(conds))
   
    def repeatition(self, n_repeats):
        self.random_repeats = np.repeat(self.conditions, n_repeats, axis = 0)
        random.shuffle(self.random_repeats)

class TestingDataHandler():
    def __init__(self, parameters, *conds):    
        self.conditions = np.array(np.meshgrid(*conds)).T.reshape(-1,len(conds))
        self.data = {}
        self.parameters = parameters
        for entry in self.conditions:
            condname = '.'.join(entry)
            paras = {}
            for p in parameters:
                paras['{}'.format(p)] = []
            self.data[condname] = paras
    
    def TrialAppend(self, trial_data, *conds):
        # Save data to data library
        condname = '.'.join([*conds])
 
        for i in np.arange(len(trial_data)):
            self.data[condname][self.parameters[i]].append(trial_data[i])

cond1 = ['tactile', 'non_tactile']
cond2 = ['experimental', 'control']
ps = ['rt', 'temperature']

a = TestingDataHandler(ps, cond1, cond2)

# a = ConditionsHandler(cond1, cond2)

rt = 1
tm = 2

trial_data = [rt, tm]

a.TrialAppend(trial_data, cond1[1], cond2[0])
print(a.data)


self.data[[*llaves_data][0]].keys()
for k,v in zip(data[cond_string].items(), np.arange(len(data_trial))):
    v.append(data_trial[j])

data = {'tactile.experimental': {'rt': [1, 2, 3], 'temperature': [5, 6, 7]},
        'tactile.control': {'rt': [1, 23, 4], 'temperature': [7, 89, 9]},
        'non_tactile.experimental': {'rt': [1, 1, 1], 'temperature': [80, 10, 20]},
        'non_tactile.control': {'rt': [1, 1, 1], 'temperature': [1, 1, 1]}
    }


saveIndv('tt', 'tests', data)


raw = pd.read_csv('./tests/pp.csv')

from classes_arduino import ArdUIno

arduino_shutter = ArdUIno(usb_port = 2, n_modem = 4)
arduino_shutter.arduino.flushInput()

shakeShutter(arduino_shutter, 5)
