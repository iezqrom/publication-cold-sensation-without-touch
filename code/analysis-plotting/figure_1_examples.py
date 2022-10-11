# %%
from classes_tharnalBeta import ReAnRaw
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3

colorMapType = 0
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation

### Data structure
import numpy as np

## Media
from imutils.video import VideoStream
from classes_tharnal import *
from plotting import *


# %%
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
# print current path
import os
print(os.getcwd())

# %%
path = "../data"
shuA = shu_temp(f"{path}/zaber7_18112019/shu8")

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
# plt.savefig('../CEP_example.pdf', transparent = True)
plt.savefig('../../../figures/methods_paper_mol/final/CEP_example.png', transparent = True)

# %% PID

path = "../data"
steps_mm = 0.00049609375
cloA = shu_temp(f"{path}/zaber8_19112019/clo10")
cloA.getParaPID()
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
# plt.savefig("./MAN_example_pos_temp.pdf", transparent=True)
plt.savefig("../../../figures/methods_paper_mol/final/MAN_example_pos_temp.png", transparent=True)

# %%


# %% ANIMATION CEP
start = 30
end = 222

Writer = animation.writers["ffmpeg"]
writer = Writer(fps=9, metadata=dict(artist="Me"), bitrate=1800)

dummy = 0


def animate(i, shuA, plots, axes, shutter, means):
    vminT = 25
    vmaxT = 34
    print(i)

    widthtick = 3
    title_pad = 20

    lwD = 5
    widthtick = 5
    lenD = 15
    s_bub = 150

    try:
        dataK = shuA.read["image" + str(i + 30) + "_open"][:]
        OnOff = 1
    except KeyError:
        dataK = shuA.read["image" + str(i + 30) + "_close"][:]
        OnOff = 0

    scep = np.asarray(shutter)
    idx_shu = np.where(scep == 1)

    # print('here')

    # frame +=1

    # print(dataK)
    dataC = (dataK - 27315) / 100
    r = 40

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

    # shutter.append(OnOff)
    # means.append(mean)

    Xin, Yin = np.mgrid[0:120, 0:160]

    # First subplot: 2D RAW
    ax1.clear()

    minC = np.min(dataC)
    # minC = (min - 27315) / 100
    indx, indy = np.where(dataC == minC)

    circles = []

    xsC = np.arange(0, 160)
    ysC = np.arange(0, 120)

    for a, j in zip(indx, indy):
        cirD = plt.Circle((j, a), r, color="b", fill=False, lw=lwD * 1.2)
        circles.append(cirD)

    mask = (xsC[np.newaxis, :] - indy[0]) ** 2 + (
        ysC[:, np.newaxis] - indx[0]
    ) ** 2 < r ** 2
    roiD = dataC[mask]
    # plt.rcParams.update({'font.size': 20})

    ax1.imshow(dataC, cmap="hot", vmin=vminT, vmax=vmaxT)
    ax1.add_artist(circles[0])

    ax1.set_title("Thermal image", pad=title_pad)

    ax1.set_axis_off()

    # ax1.spines['top'].set_visible(False)
    # ax1.spines['right'].set_visible(False)
    # ax1.spines['left'].set_visible(False)
    # ax1.spines['bottom'].set_visible(False)

    # Third subplot: Max means
    ax3.clear()
    # ax3 = fig.add_subplot(2, 2, 3, projection = '3d')
    # print(dummy)
    ax3.plot(means[0 : i + 1], lw=lwD * 1.2, color="#658DC6")
    ax3.set_ylim(vminT, vmaxT)
    ax3.set_xlim([0, len(means)])

    ax3.set_title("Mean Temperature in ROI", pad=title_pad)

    fill_shade = np.zeros(len(means))
    fi = idx_shu[0][idx_shu[0] < i]
    fill_shade[fi] = 34

    ax3.fill_between(np.arange(len(means)), fill_shade, y2=0, color="k", alpha=0.25)

    steps = 2
    #
    framesToseconds(ax3, 2, means)

    ax3.set_yticks(np.arange(25, 34.01, 1))

    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    ax3.yaxis.set_tick_params(width=lwD, length=lenD)
    ax3.xaxis.set_tick_params(width=lwD, length=lenD)

    ax3.tick_params(axis="y", which="major", pad=10)
    ax3.tick_params(axis="x", which="major", pad=10)

    ax3.spines["left"].set_linewidth(lwD)
    ax3.spines["bottom"].set_linewidth(lwD)

    ax3.set_ylabel("Temperature ($^\circ$C)", labelpad=20)
    ax3.set_xlabel("Time (s)", labelpad=20)
    plt.tight_layout()


################ Plot figure
fig = plt.figure(figsize=(35, 10))

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

#######################Axes
ax1 = fig.add_subplot(121)
ax3 = fig.add_subplot(122)

x = np.arange(0, 160, 1)
y = np.arange(0, 120, 1)

xs, ys = np.meshgrid(x, y)
zs = (xs * 0 + 15) + (ys * 0 + 15)

vminT = 25
vmaxT = 34
######################Plots
## First subplot: 2D video
plot1 = ax1.imshow(zs, cmap="hot", vmin=vminT, vmax=vmaxT)
cb = fig.colorbar(plot1, ax=ax1)
cb.set_ticks(np.arange(25, 34.01, 1))

## Third subplot: Contour + Gaussian fit
shutterC = shuA.shutterOnOff[start:end]
meansC = shuA.means[start:end]

plot3 = ax3.plot(np.arange(len(meansC)), np.arange(len(meansC)), color="#007CB7")

plots = [plot1, plot3]

# Aesthetics
axes = [ax1, ax3]
plt.tight_layout()

# scep = np.asarray(shu_CEP)
# idx_shu = np.where(scep == 1)

# y_dat = means_CEP[:-3]

# ax.plot(np.arange(len(y_dat)), y_dat, lw = lwD*1.2, color = '#658DC6')

# framesToseconds(ax, 2, y_dat)
# ax.set_xlim([0, len(y_dat)])
# ax.set_ylim([25, 34])

# fill_shade = np.zeros(len(means_CEP))
# fill_shade[idx_shu] = 34

# Animation & save
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=len(shuA.means[start:end]),
    fargs=(shuA, plots, axes, shutterC, meansC),
    interval=1000 / 8.7,
)

ani.save("../neuro_methods_paper/colther_evoked_3.mp4", writer=writer)

# %%
start = 0
end = 523

# plt.plot(np.arange(len(medium.max_mean[start:end])), medium.max_mean[start:end], color =  '#007CB7', lw = 3) #5F4B8B )

Writer = animation.writers["ffmpeg"]
writer = Writer(fps=9, metadata=dict(artist="Me"), bitrate=1800)


def animate(i, cloA, plots, axes, shutter, means, zaber):

    vminT = 25
    vmaxT = 34
    print(i)

    widthtick = 3
    title_pad = 20

    lwD = 5
    widthtick = 5
    lenD = 15
    s_bub = 150

    dataAll = cloA.read["image" + str(i + 1)][:]

    dataK = dataAll[0:120]

    scep = np.asarray(shutter)
    idx_shu = np.where(scep == 1)

    dataC = (dataK - 27315) / 100
    r = 20

    minimoK = np.min(dataK)
    minimoC = (minimoK - 27315) / 100

    xs = np.arange(0, 160)
    ys = np.arange(0, 120)

    indx, indy = np.where(dataC == minimoC)
    # print(indx, indy)

    mask = (xs[np.newaxis, :] - indy[0]) ** 2 + (
        ys[:, np.newaxis] - indx[0]
    ) ** 2 < r ** 2
    roiC = dataC[mask]
    mean = round(np.mean(roiC), 2)

    # shutter.append(OnOff)
    # means.append(mean)

    Xin, Yin = np.mgrid[0:120, 0:160]

    # First subplot: 2D RAW
    ax1.clear()

    minC = np.min(dataC)
    # minC = (min - 27315) / 100
    indx, indy = np.where(dataC == minC)

    circles = []

    xsC = np.arange(0, 160)
    ysC = np.arange(0, 120)

    for a, j in zip(indx, indy):
        cirD = plt.Circle((j, a), r, color="b", fill=False, lw=lwD * 1.2)
        circles.append(cirD)

    ax1.imshow(dataC, cmap="hot", vmin=vminT, vmax=vmaxT)
    ax1.add_artist(circles[0])

    ax1.set_title("Thermal image", pad=title_pad)

    ax1.set_axis_off()

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)

    # Third subplot: Max means
    ax3.clear()

    ax3.plot(means[0 : i + 1], lw=lwD, color="#658DC6")
    ax3.set_ylim(vminT, vmaxT)
    ax3.set_xlim(0, len(means))
    ax3.xaxis.set_tick_params(width=widthtick)
    ax3.yaxis.set_tick_params(width=widthtick)

    ax3.set_ylabel("Temperature ($^\circ$C)", labelpad=20)
    ax3.set_xlabel("Time (s)", labelpad=20)

    ax3.set_title("Mean Temperature in ROI", pad=title_pad)

    framesToseconds(ax3, 4, means)

    ax3.set_yticks(np.arange(25, 34.01, 1))

    ax3.spines["top"].set_visible(False)
    # ax3.spines['right'].set_visible(False)

    ax3.yaxis.set_tick_params(width=lwD, length=lenD)
    ax3.xaxis.set_tick_params(width=lwD, length=lenD)

    ax3.tick_params(axis="y", which="major", pad=10)
    ax3.tick_params(axis="x", which="major", pad=10)

    ax3.spines["left"].set_linewidth(lwD)
    ax3.spines["bottom"].set_linewidth(lwD)

    ax3.set_ylabel("Temperature ($^\circ$C)", labelpad=20)
    ax3.set_xlabel("Time (s)", labelpad=20)
    plt.tight_layout()

    # ax4 = ax3.twinx()
    # lns_alc = ax4.plot(zaber[0:i + 1], color='k')

    # shutterE = np.repeat(0, repeats = len(zaber))
    # ind = np.where(np.asarray(shutterC[0:i + 1]) == 1)

    # shutterE[ind] = np.max(zaber)

    fill_shade = np.zeros(len(means))
    fi = idx_shu[0][idx_shu[0] < i]
    fill_shade[fi] = 34

    ax3.fill_between(np.arange(len(means)), fill_shade, y2=0, color="k", alpha=0.25)

    # ax2.set_ylim([0, 1.1])
    # ax4.set_ylabel('Zaber position')

    # frames = np.arange(0, len(shutter))
    # seconds = np.arange(0, round(len(shutter)/8.7*1000), round(1000/8.7))

    ax3.set_xlim(0, len(means))
    ax3.axhline(27, color="r", lw=2, linestyle="--")
    ax3.annotate(
        "Set-point", xy=(4, 26.95), xytext=(3.8, 26), arrowprops=dict(arrowstyle="->")
    )

    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)


################ Plot figure
fig = plt.figure(figsize=(35, 10))
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

#######################Axes
ax1 = fig.add_subplot(121)
# ax2 = fig.add_subplot(132, projection = '3d')
ax3 = fig.add_subplot(122)
# ax4 = ax3.twinx()

x = np.arange(0, 160, 1)
y = np.arange(0, 120, 1)

xs, ys = np.meshgrid(x, y)
zs = (xs * 0 + 15) + (ys * 0 + 15)

vminT = 25
vmaxT = 34
######################Plots
## First subplot: 2D video
plot1 = ax1.imshow(zs, cmap="hot", vmin=vminT, vmax=vmaxT)
cb = fig.colorbar(plot1, ax=ax1)
cb.set_ticks(np.arange(25, 34.01, 1))

# ## Second subplot: 3D Raw
# plot2 = ax2.plot_surface(xs, ys, zs, rstride=1, cstride=1, cmap='hot', vmin = vminT, vmax = vmaxT)
# cbar = fig.colorbar(plot2, ax = ax2)
# cbar.set_label('Temperature ($^\circ$C)')

## Third subplot: Contour + Gaussian fit
# shutterC = cloA.shutterOnOff[:]
meansC = cloA.means[start:end]
zaberC = cloA.zaber_pos[start:end]
shutterC = np.asarray(cloA.shutterOnOff[start:end])

plot3 = ax3.plot(np.arange(len(meansC)), np.arange(len(meansC)), color="#658DC6", lw=4)
# fig.colorbar(plot3, ax = ax3)

# plot4 = ax4.plot(np.arange(len(zaberC)), np.arange(len(zaberC)), color =  'k', lw = 4 )

# ax4.spines['top'].set_visible(False)

plots = [plot1, plot3]

# Aesthetics
axes = [ax1, ax3]

# Animation & save
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=len(meansC),
    fargs=(cloA, plots, axes, shutterC, meansC, zaberC),
    interval=1000 / 8.7,
)

ani.save("../neuro_methods_paper/colther_PID.mp4", writer=writer)

# %%
