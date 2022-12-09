# %%
import matplotlib.pyplot as plt
import numpy as np

from plotting import plotParams, framesToseconds
from globals import path_data, path_figures, colour_blue
from local_functions import shu_temp

plotParams()

lwD = 7
widthtick = 10
lenD = 20
s_bub = 150

# %%
path_data_examples = path_data + "/examples/scenario2_examples"
data = {}
name_files = [f"example{i}" for i in range(1, 5)]


fig, ax = plt.subplots(1, 1, figsize=(20, 10))
for name_file in name_files:
    print(name_file)
    data[name_file] = {}
    data[name_file]['data'] = shu_temp(f"{path_data_examples}/{name_file}")
    data[name_file]['data'].getParaPID()

    data[name_file]['traces_start_end'] = []
    data[name_file]['traces'] = []
    data[name_file]['shifted_traces'] = []

    # plot each iteration in a different plot
    if len(data[name_file]['data'].means) > 600:
        cut_end = -298
        y_dat = data[name_file]['data'].means[:cut_end]
    else:
        cut_end = -2
    ax.plot(np.arange(len(data[name_file]['data'].means[:cut_end])), data[name_file]['data'].means[:cut_end], color=colour_blue, lw=lwD * 1.2)
    print(len(data[name_file]['data'].means[:cut_end]))

ax.set_xlim([0, 530])
ax.set_yticks(np.arange(24, 34.01, 2))

name_file = "scenario2_mainexample"
cloA = shu_temp(f"{path_data}/examples/{name_file}")
cloA.getParaPID()

steps_mm = 0.00049609375
zaber_offset = 302362 - np.max(cloA.zaber_pos)
max_list_cm = (zaber_offset * steps_mm + 40) / 10

transformed_zabers_axis = [np.max(cloA.zaber_pos) - pos for pos in cloA.zaber_pos]
transformed_axis_mm = [tza * steps_mm for tza in transformed_zabers_axis]

transformed_axis_cm = [tam / 10 + max_list_cm for tam in transformed_axis_mm]

ax2 = ax.twinx()
ax2.plot(transformed_axis_cm, lw=lwD * 1.2, color="k")
ax.set_zorder(ax2.get_zorder() + 1)

ax.patch.set_visible(False)
ax2.set_ylim([0, 20])
ax2.set_yticks(np.arange(0, 20.01, 5))
framesToseconds(ax, 5, y_dat, int)  # np.max(self.objs_mean_temp))
ax.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.axhline(27, color="#B75E41", linewidth=5, linestyle="--")

ax.yaxis.set_tick_params(width=lwD, length=lenD)
ax.xaxis.set_tick_params(width=lwD, length=lenD)
ax2.yaxis.set_tick_params(width=lwD, length=lenD)

ax.tick_params(axis="y", which="major", pad=10, color='lightgrey')
ax.tick_params(axis="x", which="major", pad=10, color='lightgrey')
ax2.tick_params(axis="y", which="major", pad=10, color='lightgrey')

ax.spines["left"].set_linewidth(lwD)
ax.spines["bottom"].set_linewidth(lwD)
ax2.spines["right"].set_linewidth(lwD)

for spine in ax.spines.values():
    spine.set_edgecolor('lightgrey')

for spine in ax2.spines.values():
    spine.set_edgecolor('lightgrey')

ax.set_ylabel("Temperature ($^\circ$C)", labelpad=20, color="#658DC6")
ax.set_xlabel("Time (s)", labelpad=20)
ax2.set_ylabel("Distance nozzle - skin (cm)", labelpad=20)
ax2.set_zorder(1)
plt.tight_layout()

plt.savefig(f'{path_figures}/figure1/panelC_scenario2_with_examplerobot.png', transparent=True)


# %% PID
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

# secondar y axis
ax2 = ax.twinx()
ax2.plot(transformed_axis_cm, lw=lwD * 1.2, color="k")
ax2.set_yticks(np.arange(0, 20, 5))

framesToseconds(ax, 5, y_dat, int)  # np.max(self.objs_mean_temp))
ax.spines["top"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.axhline(27, color="#B75E41", linewidth=5, linestyle="--")

ax.yaxis.set_tick_params(width=lwD, length=lenD)
ax.xaxis.set_tick_params(width=lwD, length=lenD)
ax2.yaxis.set_tick_params(width=lwD, length=lenD)

ax.tick_params(axis="y", which="major", pad=10, color='lightgrey')
ax.tick_params(axis="x", which="major", pad=10, color='lightgrey')
ax2.tick_params(axis="y", which="major", pad=10, color='lightgrey')

ax.spines["left"].set_linewidth(lwD)
ax.spines["bottom"].set_linewidth(lwD)
ax2.spines["right"].set_linewidth(lwD)

for spine in ax.spines.values():
    spine.set_edgecolor('lightgrey')

for spine in ax2.spines.values():
    spine.set_edgecolor('lightgrey')

ax.set_ylabel("Temperature ($^\circ$C)", labelpad=20, color="#658DC6")
ax.set_xlabel("Time (s)", labelpad=20)
ax2.set_ylabel("Distance needle - skin (cm)", labelpad=20)
ax2.set_zorder(1)
plt.tight_layout()


# %%
