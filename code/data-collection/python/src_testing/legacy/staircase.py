import matlab.engine as me
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

if __name__ == "__main__":

    eng = me.start_matlab()
    alphas = np.arange(28, 32, 1)

    alphas_list = list(alphas)

    alphas_ll = []
    for i in alphas_list:
        alphas_ll.append(round(i, 2))

    alphas_ll = [float(i) for i in alphas_ll]

    RF = eng.quest_matlab_set_up(alphas_ll, nargout=1)

    temp = 30

    array_RFS = []

    while RF["stop"] == 0:
        start_reply = time.time()
        answer = input("Did it feel cold? ")
        end_reply = time.time()

        time_reply = end_reply - start_reply

        if answer == "y":
            response = 0
        elif answer == "n":
            response = 1

        RF = eng.quest_matlab_update(RF, temp, response)

        temp = RF["xCurrent"]
        print(temp)
        time.sleep(1)
        array_RFS.append(RF)

temps = np.asarray(RF["x"])

temps
cs = np.repeat(1, len(temps[0]))
response = np.asarray(RF["response"])
cs[np.where(response)[1]] = 0
classes = ["No", "Yes"]
colours = ListedColormap(["r", "g"])

fig, ax = plt.subplots(figsize=(15, 20))
scatter = ax.scatter(np.arange(len(temps[0])), temps[0], c=cs, cmap=colours)
plt.legend(handles=scatter.legend_elements()[0], labels=classes)
ax.set_yticks(np.arange(30, 31.6, 0.1))
ax.set_ylabel("Temperature")
ax.set_xlabel("Trials")

plt.savefig("quest_steps.png")


legend1 = ax.legend(*scatter.legend_elements(), loc="lower left", title="Classes")
ax.add_artist(legend1)

handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)

legend2 = ax.legend(handles, labels, loc="upper right", title="Sizes")
