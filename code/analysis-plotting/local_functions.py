import numpy as np
import matplotlib.pyplot as plt
import h5py
from tharnal import ReAnRaw
from globals import colour_blue

class shu_temp(ReAnRaw):
    def __init__(self, input):
        self.read = h5py.File("{}.hdf5".format(input), "r")

    def getPara(self):

        self.min_pixel = []
        self.means = []
        self.peak_pos = []
        # self.poses = []
        self.shus = []
        self.shutterOnOff = []

        r = 20
        frame = 1

        for i in np.arange(len(self.read.keys())):

            try:
                dataK = self.read["image" + str(frame) + "_open"][:]
                OnOff = 1
            except KeyError:
                dataK = self.read["image" + str(frame) + "_close"][:]
                OnOff = 0

            frame += 1

            # print(dataK)
            dataC = (dataK - 27315) / 100

            minimoK = np.min(dataK)
            minimoC = (minimoK - 27315) / 100
            # print(dataC)

            xs = np.arange(0, 160)
            ys = np.arange(0, 120)

            indx, indy = np.where(dataC == minimoC)
            # print(indx, indy)

            mask = (xs[np.newaxis, :] - indy[0]) ** 2 + (
                ys[:, np.newaxis] - indx[0]
            ) ** 2 < r ** 2
            roiC = dataC[mask]
            mean = round(np.mean(roiC), 2)

            self.means.append(mean)
            self.min_pixel.append(minimoC)
            self.shutterOnOff.append(OnOff)

    def plot(self, start=0, end=10000):
        fig, ax = plt.subplots(figsize=(20, 10))
        plt.rcParams.update({"font.size": 20})

        plt.plot(np.arange(len(self.means)), self.means)

        ax2 = ax.twinx()
        lns_alc = ax2.plot(
            np.arange(len(self.shutterOnOff[start:end])),
            self.shutterOnOff[start:end],
            color="k",
        )

    def getParaPID(self):

        self.min_pixel = []
        self.means = []
        self.peak_pos = []
        # self.poses = []
        self.shus = []
        self.shutterOnOff = []
        self.zaber_pos = []

        r = 20
        frame = 1

        for i in np.arange(len(self.read.keys())):

            dataAll = self.read["image" + str(frame)][:]
            dataK = dataAll[0:120]

            pos = dataAll[120]
            posState = pos[0]

            shutter = dataAll[121]
            OnOff = shutter[0]

            frame += 1

            # print(dataK)
            dataC = (dataK - 27315) / 100

            minimoK = np.min(dataK)
            minimoC = (minimoK - 27315) / 100
            # print(dataC)

            xs = np.arange(0, 160)
            ys = np.arange(0, 120)

            indx, indy = np.where(dataC == minimoC)
            # print(indx, indy)

            mask = (xs[np.newaxis, :] - indy[0]) ** 2 + (
                ys[:, np.newaxis] - indx[0]
            ) ** 2 < r ** 2
            roiC = dataC[mask]
            mean = round(np.mean(roiC), 2)

            self.means.append(mean)
            self.min_pixel.append(minimoC)
            self.shutterOnOff.append(OnOff)
            self.zaber_pos.append(posState)

        shus = np.asarray(self.shutterOnOff)
        self.open, self.close = np.where(shus[:-1] != shus[1:])[0]

        self.open = self.open + 1
        self.close = self.close + 1

        # print(dataC)

def indvidual_trace_assesment(data, example):
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    ax.plot(data[example]['data'].means)
    # another y axis
    ax2 = ax.twinx()
    ax2.plot(data[example]['data'].shutterOnOff)

    data[example]['traces'] = []
    for start_end in data[example]['traces_start_end']:
        ax.axvspan(start_end[0], start_end[1], alpha=0.5, color='red')
        print(start_end[1] - start_end[0])
        data[example]['traces'].append(data[example]['data'].means[start_end[0]:start_end[1]])

    data[example]['traces'] = np.array(data[example]['traces'])


    for start_end in data[example]['traces_start_end']:
        fig, ax = plt.subplots(1, 1, figsize=(20, 10))
        ax.plot(data[example]['data'].means[start_end[0]:start_end[1]])
        ax.axvline(5, color = 'black', linestyle = '--')

    # %%  
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    for start_end in data[example]['traces_start_end']:
        ax.plot(data[example]['data'].means[start_end[0]:start_end[1]], color = colour_blue)

    # %% normalise traces
    def standardise(data, example):
        mean_traces = np.mean(data[example]['traces'][:, 0:3])
        diff_traces = np.mean(mean_traces - data[example]['traces'][:, 0:3], axis = 1)
        data[example]['shifted_traces'] = []
        print(diff_traces)

        for index, trace in enumerate(data[example]['traces']):
            data[example]['shifted_traces'].append((trace + diff_traces[index]))

        data[example]['shifted_traces'] = np.array(data[example]['shifted_traces'])
        return data

    data = standardise(data, example)

    # %%  
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))

    ax.plot(data[example]['shifted_traces'].T, color = colour_blue)
    # ax.plot(np.mean(data[example]['shifted_traces'].T, axis=1), color = 'black')
    # vertical line
    ax.axvline(5, color = 'black', linestyle = '--')

    # %%
    # calculate slope of signal

    data[example]['slope'] = []
    for trace in data[example]['shifted_traces']:
        data[example]['slope'].append(np.mean(np.diff(trace[5:7])))

    print(data[example]['slope'])