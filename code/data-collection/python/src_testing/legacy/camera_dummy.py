# #!/usr/bin/env python3
#

import time
import numpy as np

from tkinter import *
import globals
from experiment import experiment

try:
    from queue import Queue
except ImportError:
    from Queue import Queue

BUF_SIZE = 2
q = Queue(BUF_SIZE)


def camera_dummy():
    cam = TherCam()
    cam.startStream()

    ax = globals.fig.add_subplot(111)
    globals.fig.tight_layout()

    current_cmap = plt.cm.get_cmap()
    current_cmap.set_bad(color="black")
    print("start thread")

    while True:

        data = q.get(True, 500)
        print("we are here")
        if data is None:
            print("Data is none")
            exit(1)

        # We save the data
        minimoK = np.min(data)
        minimo = (minimoK - 27315) / 100

        data = (data - 27315) / 100

        # img.set_data(data)
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.imshow(data, vmin=globals.vminT, vmax=globals.vmaxT)
        print(data)
        plt.pause(0.0005)

        # print('we are printing')

        if cv2.waitKey(1) & keyboard.is_pressed("enter"):
            cv2.destroyAllWindows()
            print("Stop streaming")
            libuvc.uvc_stop_streaming(devh)

    # except Exception as e:
    #     print(e)

    print("end thread")
