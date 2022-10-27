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
path_data_examples = path_data + "/examples/scenario3_examples"
data = {}
name_files = [f"example{i}" for i in range(1, 6)]

for name_file in name_files:
    data[name_file] = {}
    data[name_file]['data'] = shu_temp(f"{path_data_examples}/{name_file}")
    data[name_file]['data'].getPara()

    data[name_file]['traces_start_end'] = []
    data[name_file]['traces'] = []
    data[name_file]['shifted_traces'] = []

    # plot each iteration in a different plot
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    ax.plot(np.arange(len(data[name_file]['data'].means)), data[name_file]['data'].means)

# %%

data['example1']['traces_start_end'] = [(247, 281)]
data['example2']['traces_start_end'] = []
data['example3']['traces_start_end'] = [(91, 125)]
data['example4']['traces_start_end'] = []
data['example5']['traces_start_end'] = [(72, 106), (150, 184), (227, 261)]

for example in name_files:
    data[example]['traces'] = []
    for start_end in data[example]['traces_start_end']:
        ax.axvspan(start_end[0], start_end[1], alpha=0.5, color='red')
        print(start_end[1] - start_end[0])
        data[example]['traces'].append(data[example]['data'].means[start_end[0]:start_end[1]])

    data[example]['traces'] = np.array(data[example]['traces'])


# %% plot them all together
all_traces = []
for example in name_files:
    temp_traces = data[example]['traces']
    if len(temp_traces) > 0:
        all_traces.append(temp_traces)

all_traces = np.concatenate(all_traces)

all_shifted_traces = []

mean_traces = np.mean(all_traces[:, 0:3])
diff_traces = np.mean(mean_traces - all_traces[:, 0:3], axis = 1)
for index, trace in enumerate(all_traces):
    all_shifted_traces.append((trace + diff_traces[index]))

all_shifted_traces = np.array(all_shifted_traces)
# plot all traces
fig, ax = plt.subplots(1, 1, figsize=(20, 10))
ax.plot(all_shifted_traces.T, color = colour_blue)
# plot mean
ax.plot(np.mean(all_shifted_traces, axis = 0), color = colour_blue,  lw=lwD * 1.2,)

ax.set_yticks(np.arange(24, 34.01, 2))

framesToseconds(ax, 0.5, all_shifted_traces[0, :], float)
ax.set_xlim([0, len(all_shifted_traces[0, :])])
ax.set_ylim([25, 34])
ax.set_yticks(np.arange(24, 34.01, 2))

fill_shade = np.zeros(len(all_shifted_traces[0, :]))
fill_shade[5:31] = 34

ax.fill_between(np.arange(len(all_shifted_traces[0, :])), fill_shade, y2=0, color="k", alpha=0.25)

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


# %% plot all slopes
all_slopes = []
for trace in all_shifted_traces:
    all_slopes.append(np.mean(np.diff(trace[5:7])))
    print((trace[7] - trace[6]) /0.1)
print(all_slopes)
print(len(all_slopes))

print(np.mean(all_slopes))
print(np.std(all_slopes))



# %%
