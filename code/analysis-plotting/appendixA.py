# %%
from globals import path_data, path_figures
from tharnal import grabManyvideos, ReAnRaw
import matplotlib.pyplot as plt
from scipy import stats
from plotting import framesToseconds, prettifySpinesTicks
import matplotlib.patches as patches
import numpy as np

def multiply_by_10(x):
    if isinstance(x, float):
        return int(x * 10)
    else:
        return x

# %%
pad_size = 20
pad_size_ticks = 10
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
width_lines = 10
length_ticks = 20
# %%
def analyse_ROI(data, change_point, r = 20):
    name_image = 'image'

    min_pixel = []
    means = []
    surround = []

    for i in np.arange(len(data.data[name_image])):
        if i < change_point:
            name_coor = 'fixed_ROI'
        else:
            name_coor = 'diff_ROI'

        minimoC = np.min(data.data[name_image][i])

        xs = np.arange(0, 160)
        ys = np.arange(0, 120)

        try:
            cs = data.data[name_coor][i][:, 0]
            cy = cs[1]
            cx = cs[0]
        except:
            cs = data.data[name_coor][i]
            cy = cs[1]
            cx = cs[0]

        mask = (xs[np.newaxis,:] - cy)**2 + (ys[:,np.newaxis] - cx)**2 < r**2

        roiC = data.data[name_image][i][mask]
        mean = round(np.mean(roiC), 2)

        unmask = np.invert(mask)
        unroiC = data.data[name_image][i][unmask]
        meanSU = round(np.mean(unroiC), 2)

        means.append(mean)
        min_pixel.append(minimoC)
        surround.append(meanSU)

    return means


# %%

folder_name = f"appendixA"
lut_distances = [3.5, 4, 4.5, 5, 5.5, 6]
dict_lut_distances = {}

# for ns, ta in enumerate(lut_distances):
names = grabManyvideos(path_data, folder_name, pattern="lut_distance_.*\.hdf5$")

# iterate over lut_distances
for ns, ta in enumerate(lut_distances):
    mta = multiply_by_10(ta)
    dict_lut_distances[mta] = []
    for name in names:
        # split name
        name_split = name.split("_")
        if name_split[2] == str(mta):
            print(name)
            dat_im = ReAnRaw(f"{path_data}/{folder_name}/videos/{name}")
            dat_im.datatoDic()
            if ta == 3.5:
                change_point = 0
            else:
                change_point = 16
            means = analyse_ROI(dat_im, change_point)
            # dat_im.extractMeans(name_coor="diff_ROI")
            dict_lut_distances[mta].append(means)

for k, v in dict_lut_distances.items():
    temp_means = []
    for i, j in enumerate(v):
        temp_means.append(j[0:88])

    mean_temp_means = np.mean(temp_means, axis=0)
    dict_lut_distances[k] = {"mean": []}
    dict_lut_distances[k]["mean"] = mean_temp_means

# %%
# drop plot
drops_to_plot = [35, 5, 6]
names = [f"{drops_to_plot[0]/10}", f"{drops_to_plot[1]}", f"{drops_to_plot[2]}"]
colors = ["#8AA3AF", "#8B94C1", "#751C77"]

fig, ax = plt.subplots(figsize=(10, 10))

for i_drop, drop in enumerate(drops_to_plot):
    ax.plot(
        dict_lut_distances[drop]["mean"],
        label=f"{names[i_drop]}",
        linewidth=width_lines,
        color=colors[i_drop],
    )

framesToseconds(ax, 2, dict_lut_distances[drop]["mean"])

# change position legend
leg = ax.legend(bbox_to_anchor=(1, 1.3), title = "Nozzle-skin\ndistance (cm)")
leg.get_frame().set_linewidth(0.0)
leg.get_frame().set_alpha(0)

ax.set_ylabel("Temperature ($^\circ$C)", labelpad=pad_size)
ax.set_xlabel("Time (s)", labelpad=pad_size)

# # remove outline legend
# ax.legend(frameon=False)
# change thickness of axes
ax.spines["left"].set_linewidth(width_lines)
ax.spines["bottom"].set_linewidth(width_lines)
# change size of ticks
ax.tick_params(axis="both", which="major", width=width_lines, length=length_ticks)
# limit x axis
ax.set_xlim(0, 87)
ax.set_ylim(23, 35)
# change y ticks
ax.set_yticks(np.arange(23, 36, 2))
# change pad ticks
ax.tick_params(axis="x", pad=pad_size_ticks)
ax.tick_params(axis="y", pad=pad_size_ticks)

# fill in
x = np.array([78, 88])
y1 = np.array([25.8, 25.8])
y2 = np.array([27, 27])
start_rectangle = 78

for i_drop, drop in enumerate(drops_to_plot):
    last_mean = np.mean(dict_lut_distances[drop]["mean"][-10:])
    # draw rectangle in graph
    wiggle_room = 0.5
    y1 = np.array([last_mean - wiggle_room, last_mean - wiggle_room])
    y2 = np.array([last_mean + wiggle_room, last_mean + wiggle_room])
    print(last_mean)
    rect = patches.Rectangle(
        (start_rectangle, (last_mean - wiggle_room)),
        8.6,
        1,
        linewidth=5,
        edgecolor='black',
        facecolor='none'
    )
    ax.add_patch(rect)

# Add the patch to the Axes
ax.fill_between(
    [15, 88],
    0,
    35,
    facecolor="black",
    alpha=0.2,
    edgecolor='black',
    linewidth=1,
)

# remove top and right borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

prettifySpinesTicks(ax, colour = 'grey')
plt.savefig(f"{path_figures}/{folder_name}/appendixA_drop_analysis.png", transparent=True, bbox_inches='tight')

# %%
# linear regression
# iterate over dict_lut_distances
end_means = []
for k, v in dict_lut_distances.items():
    # get the last 10 values of means in dict_lut_distances
    last_10_means = v["mean"][-10:]
    # mean of last 10 values
    mean_last_10 = np.mean(last_10_means)
    # append to end_means
    end_means.append(mean_last_10)

# %%
# linear regression plot
fig, ax = plt.subplots(figsize=(10, 10))

# linear regression on end_means
slope, intercept, r_value, p_value, std_err = stats.linregress(lut_distances, end_means)
# build line for plotting
line = [slope * ld + intercept for ld in lut_distances]
# plot
ax.plot(lut_distances, line, linewidth=width_lines, color="black")
# plot end_means
ax.scatter(lut_distances, end_means, s=200, color="grey", zorder = 10)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_ylabel("Temperature ($^\circ$C)", labelpad=pad_size)
ax.set_xlabel("Distance (cm)", labelpad=pad_size)

# limit x axis
ax.set_xlim(3, 7)
ax.set_ylim(23, 35)

# change thickness of axes
ax.spines["left"].set_linewidth(width_lines)
ax.spines["bottom"].set_linewidth(width_lines)

# change y ticks
ax.set_yticks(np.arange(23, 36, 2))
ax.set_xticks(np.arange(3, 8, 1))
# change pad of y and x ticks
ax.tick_params(axis="both", which="major", width=width_lines, length=length_ticks)

# change pad ticks
ax.tick_params(axis="x", pad=pad_size_ticks)
ax.tick_params(axis="y", pad=pad_size_ticks)

prettifySpinesTicks(ax, colour ='grey')

plt.savefig(f"{path_figures}/{folder_name}/appendixA_linear_regression.png", transparent=True, bbox_inches='tight')

# %%
