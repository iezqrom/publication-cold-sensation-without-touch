# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from text import *
import os
from tharnal import *
import random
import scipy

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
# %% Set up paths and variables for plot and analysis
path_data = "../../data/participants_mol/"
path_figures = "../../figures/"
# list folders in path
folders = os.listdir(path_data)
# remove hidden files
participant_folders = [f for f in folders if not f.startswith(".")]

lwD = 7
widthtick = 5
lenD = 20
s_bub = 350
ultraviolet = "#654EA3"
mystililac = "#BCB4C4"
driedmoss = "#CDBC7E"

pattern = f"mol_.*\.hdf5$"

patternc = re.compile(pattern)

all_deltas = []
all_baselines = []
slopes = []
coeffs = []
p_values = []
all_thresholds = []
list_lists_deltas = []
discarded_trials = {}

# %%
for folder_name in participant_folders:
    names = []
    print(folder_name)
    for filename in os.listdir(f"{path_data}/{folder_name}/"):

        if patternc.match(filename):
            name, form = filename.split(".")
            names.append(name)
        else:
            # print(filename)
            continue

    names.sort(key=natural_keys)

    delta_list = []
    baseline_list = []
    threshold_list = []
    n_discarded_trials = 0

    for i, name in enumerate(names):
        print(name)
        dat_im = ReAnRaw(f"{path_data}/{folder_name}/{name}")
        dat_im.datatoDic()
        dat_im.extractMeans()

        dat_im.extractOpenClose("stimulus")
        if len(dat_im.open) > 0:
            baseline = np.mean(dat_im.means[: (dat_im.open[0] + 1)])
            # print(baseline)

            dat_im.extractMeans(name_coor="diff_coor")
            diff_means = dat_im.means
            threshold = dat_im.means[-1]

            delta_indv = baseline - threshold

            if delta_indv > 0.2:
                delta_list.append(delta_indv)
                baseline_list.append(baseline)
                threshold_list.append(threshold)

            else:
                n_discarded_trials += 1
                print("DELTA BELOW")
        else:
            n_discarded_trials += 1
            print("Shutter didn't open")

    list_lists_deltas.append(delta_list)
    threshold_subj = np.mean(threshold_list)
    delta_subj = np.mean(delta_list)
    baseline_subj = np.mean(baseline_list)
    discarded_trials[folder_name] = n_discarded_trials

    all_deltas.append(delta_subj)
    all_baselines.append(baseline_subj)
    all_thresholds.append(threshold_subj)

# %%
# ALL DELTAS
delta_popu = np.mean(all_deltas)
fig, ax = plt.subplots(1, 1, figsize=(7, 10))

lwD = 7
widthtick = 5
lenD = 20
s_bub = 350

for dd in all_deltas:
    x_pos = random.uniform(0.95, 1.05)
    # print(x_pos)
    ax.scatter(x_pos, -dd, s=s_bub, color=ultraviolet)

ax.plot([0.95, 1.05], [-delta_popu, -delta_popu], linewidth=lwD, color=driedmoss)

ax.set_xlim(0.85, 1.15)
ax.set_ylim(-2, 0)

ax.set_ylabel("Relative cold threshold\n\n(ΔT $^\circ$C)", linespacing=0.6)
# ax.set_xlabel('Trial number')

# ax.axhline(delta_subj, 0, 1, linewidth=lwD, color=ultraviolet)
plt.tick_params(bottom=False, labelbottom=False)

# ax.axhline(0, 0, 8, linewidth=20, color='k', linestyle=':')

ax.yaxis.set_tick_params(width=lwD, length=lenD, color='grey')
ax.xaxis.set_tick_params(width=lwD, length=lenD, color='grey')

for spine in ax.spines.values():
    spine.set_edgecolor('grey')

ax.spines["left"].set_linewidth(lwD)
ax.spines["bottom"].set_linewidth(lwD)

ax.tick_params(axis="y", which="major", pad=10)
ax.tick_params(axis="x", which="major", pad=10)

ax.set_yticks([-2, -1.5, -1, -0.5, 0])

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig(f"{path_figures}/figure1/panelF_deltas.png", transparent=True)