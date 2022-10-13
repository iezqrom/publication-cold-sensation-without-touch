# %%
from globals import path_data, path_figures
from classes_tharnalBeta import ReAnRaw
colorMapType = 0
import matplotlib.pyplot as plt
### Data structure
import numpy as np
## Media
from tharnal import ReAnRaw
# from plotting import framesToseconds
import h5py

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


mc = "black"
plt.rcParams.update(
    {
        "font.size": 40,
        "axes.labelcolor": "{}".format(mc),
        "xtick.color": "{}".format(mc),
        "ytick.color": "{}".format(mc),
        "font.family": "sans-serif",
    }
)

# %%
name_file = "scenario3_mainexample"
shuA = shu_temp(f"{path_data}/examples/{name_file}")

shuA.getPara()

# %%
start = 30
end = 225

means_CEP = shuA.means[start:end]
shu_CEP = shuA.shutterOnOff[start:end]

scep = np.asarray(shu_CEP)
idx_shu = np.where(scep == 1)

fig, ax = plt.subplots(figsize=(16, 10))

lwD = 7
widthtick = 10
lenD = 20
s_bub = 150

y_dat = means_CEP[115:-40]

ax.plot(np.arange(len(y_dat)), y_dat, lw=lwD * 1.2, color="#658DC6")
ax.set_yticks(np.arange(24, 34.01, 2))

def framesToseconds(axis, steps, x):
    """
    Function to convert the x axis from frames to seconds:
    Parameters
        - Axis: name of the axis from the figure you want to change the x axis
        - Steps:
        - x: the independent variable (x)
    """
    steps = steps
    #
    seconds = np.arange(0, round(len(x) / 8.7 * 1, 2), round(10 / 8.7) * steps)
    frames = np.arange(0, len(x), 8.7 * steps)
    axis.xaxis.set_ticks(frames)

    labelsx = [item.get_text() for item in axis.get_xticklabels()]
    # print(seconds)
    # time.sleep(2)
    for j in enumerate(seconds):
        labelsx[j[0]] = float(j[1])

    axis.set_xticklabels(labelsx)

framesToseconds(ax, 0.5, y_dat)
ax.set_xlim([0, len(y_dat)])
ax.set_ylim([25, 34])
ax.set_yticks(np.arange(24, 34.01, 2))

fill_shade = np.zeros(len(y_dat))
fill_shade[9:36] = 34

ax.fill_between(np.arange(len(y_dat)), fill_shade, y2=0, color="k", alpha=0.25)

# Make-ups
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.yaxis.set_tick_params(width=lwD, length=lenD)
ax.xaxis.set_tick_params(width=lwD, length=lenD)

ax.tick_params(axis="y", which="major", pad=10)
ax.tick_params(axis="x", which="major", pad=10)

ax.spines["left"].set_linewidth(lwD)
ax.spines["bottom"].set_linewidth(lwD)

ax.set_ylabel("Temperature ($^\circ$C)", labelpad=20)
ax.set_xlabel("Time (s)", labelpad=20)

ax.tick_params(axis="y", which="major", pad=10, color='grey')
ax.tick_params(axis="x", which="major", pad=10, color='grey')

for spine in ax.spines.values():
    spine.set_edgecolor('grey')

plt.tight_layout()
plt.savefig(f'{path_figures}/figure1/panelD_scenario3.png', transparent = True)

# %% PID
name_file = "scenario2_mainexample"
cloA = shu_temp(f"{path_data}/examples/{name_file}")
cloA.getParaPID()

steps_mm = 0.00049609375
zaber_offset = 302362 - np.max(cloA.zaber_pos)
max_list_cm = (zaber_offset * steps_mm + 40) / 10

transformed_zabers_axis = [np.max(cloA.zaber_pos) - pos for pos in cloA.zaber_pos]
transformed_axis_mm = [tza * steps_mm for tza in transformed_zabers_axis]

transformed_axis_cm = [tam / 10 + max_list_cm for tam in transformed_axis_mm]

start = 0
end = 532

means_man = cloA.means[start:end]
shu_man = cloA.shutterOnOff[start:end]

scep = np.asarray(shu_man)
idx_shu = np.where(scep == 1)

fig, ax = plt.subplots(figsize=(20, 10))

y_dat = means_man[:-9]

ax.plot(np.arange(len(y_dat)), y_dat, lw=lwD * 1.2, color="#658DC6")
ax.set_xlim([0, len(y_dat)])
ax.set_ylim([25, 34])
ax.set_yticks(np.arange(24, 34.01, 2))

fill_shade = np.zeros(len(y_dat))
fill_shade[idx_shu] = 34

ax.fill_between(np.arange(len(y_dat)), fill_shade, y2=0, color="k", alpha=0.25)

ax2 = ax.twinx()
ax2.plot(transformed_axis_cm, lw=lwD * 1.2, color="k")
ax.set_zorder(ax2.get_zorder() + 1)
ax.patch.set_visible(False)
ax2.set_ylim([6, 20])
ax2.set_yticks(np.arange(6, 20.01, 2))

# Make-ups
def framesToseconds(axis, steps, x):
    """
    Function to convert the x axis from frames to seconds:
    Parameters
        - Axis: name of the axis from the figure you want to change the x axis
        - Steps:
        - x: the independent variable (x)
    """
    steps = steps
    #
    seconds = np.arange(0, round(len(x) / 8.7 * 1, 2), round(10 / 8.7) * steps)
    frames = np.arange(0, len(x), 8.7 * steps)
    axis.xaxis.set_ticks(frames)

    labelsx = [item.get_text() for item in axis.get_xticklabels()]
    # print(seconds)
    # time.sleep(2)
    for j in enumerate(seconds):
        labelsx[j[0]] = int(j[1])

    axis.set_xticklabels(labelsx)

framesToseconds(ax, 4, y_dat)  # np.max(self.objs_mean_temp))
ax.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.axhline(27, color="#B75E41", linewidth=5, linestyle="--")

ax.yaxis.set_tick_params(width=lwD, length=lenD)
ax.xaxis.set_tick_params(width=lwD, length=lenD)
ax2.yaxis.set_tick_params(width=lwD, length=lenD)

ax.tick_params(axis="y", which="major", pad=10, color='grey')
ax.tick_params(axis="x", which="major", pad=10, color='grey')
ax2.tick_params(axis="y", which="major", pad=10, color='grey')

ax.spines["left"].set_linewidth(lwD)
ax.spines["bottom"].set_linewidth(lwD)
ax2.spines["right"].set_linewidth(lwD)

for spine in ax.spines.values():
    spine.set_edgecolor('grey')

for spine in ax2.spines.values():
    spine.set_edgecolor('grey')

ax.set_ylabel("Temperature ($^\circ$C)", labelpad=20, color="#658DC6")
ax.set_xlabel("Time (s)", labelpad=20)
ax2.set_ylabel("Distance needle - skin (cm)", labelpad=20)
ax2.set_zorder(1)
plt.tight_layout()

plt.savefig(f'{path_figures}/figure1/panelC_scenario2.png', transparent=True)

