# %%
from globals import path_data, path_figures
import numpy as np
import matplotlib.pyplot as plt
from tharnal import ReAnRaw
from plotting import framesToseconds

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
name_file = "thermal_picture"
folder_name = "examples"
dat_im = ReAnRaw(f"{path_data}/{folder_name}/{name_file}")
dat_im.datatoDic()
dat_im.extractMeans(name_coor="fixed_ROI")
# %%
data = dat_im.means[14:-15]
fig, ax = plt.subplots(1, 1, figsize=(13, 10))

lwD = 7
widthtick = 5
lenD = 20
s_bub = 150
alpha_frame=1

ax.plot(data, lw=10, color="#658DC6")

steps = 1
framesToseconds(ax, steps, data)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_xlim([0, 36])
ax.set_ylim([32.5, 34])

ax.set_yticks([32.5, 33, 33.5, 34])

ax.tick_params(axis="y", which="major", pad=10)
ax.tick_params(axis="x", which="major", pad=10)

ax.spines["left"].set_linewidth(lwD)
ax.spines["bottom"].set_linewidth(lwD)

ax.set_xlabel("Time (s)", labelpad=20)
ax.set_ylabel("Temperature ($^\circ$C)", labelpad=20)
ax.yaxis.set_tick_params(width=lwD, length=lenD, color='lightgrey')
ax.xaxis.set_tick_params(width=lwD, length=lenD, color='lightgrey')
#change transparency of ticks
for line in ax.xaxis.get_ticklines():
    line.set_alpha(alpha_frame)
for line in ax.yaxis.get_ticklines():
    line.set_alpha(alpha_frame)

# change colour and opacity of the spines
for spine in ax.spines.values():
    spine.set_edgecolor('lightgrey')
    spine.set_alpha(alpha_frame)


ax.fill_between(
    [8.7, 40],
    0,
    35,
    facecolor="black",
    alpha=0.2,
    edgecolor='black',
    linewidth=1,
)

plt.tight_layout()
plt.savefig(
    f"{path_figures}/figure1/panelB_MOLexample.png",
    transparent=True,
)

# %%
from mpl_toolkits.axes_grid1 import make_axes_locatable

frame = 49
vminT = 32
vmaxT = 34
fig, ax = plt.subplots(1, 1, figsize=(13, 10))
im = ax.imshow(dat_im.data['image'][frame], cmap="coolwarm", vmin=vminT, vmax=vmaxT)
cir = plt.Circle([64, 71], 20, color="#CB8680", fill=False, lw=lwD * 1.2)
ax.add_artist(cir)

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=1)

cb = fig.colorbar(im, cax=cax)
cb.set_label("Temperature (°C)", labelpad=55, rotation=270)
cb.set_ticks(np.arange(vminT, (vmaxT + 0.01), 1))


cb.ax.tick_params(size = 0, width = 5)
cb.outline.set_visible(False)
ax.set_axis_off()
cb.ax.yaxis.set_tick_params(pad=10)

plt.tight_layout()

plt.savefig(
    f"{path_figures}/figure1/panelE_thermalImage.png",
    transparent=True,
)

# %%
