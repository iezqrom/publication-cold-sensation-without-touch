import tkinter

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib

matplotlib.use("TkAgg")

import numpy as np
import keyboard
import mplcursors
import cv2


import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

np.random.seed(42)
from classes_camera import TherCam

import h5py

# #!/usr/bin/env python3
#

import time
import numpy as np

from camera_dummy import camera_dummy

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import cv2
from imutils.video import VideoStream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation


from classes_colther import Zaber
from classes_screen import InputScreen
from classes_camera import TherCam
import time
import threading
import keyboard

# import tkinter as tk                # python 3
# from tkinter import font  as tkfont # python 3

from tkinter import *
import globals
from experiment import experiment

import matplotlib as mpl

mpl.rc("image", cmap="hot")


import tkinter as tk
from tkinter.ttk import Notebook
from tkinter import Canvas
from tkinter import messagebox as msg

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.widgets import Slider, Button, RadioButtons


def toggle_entry():
    global hidden
    if hidden:
        e.grid()
    else:
        e.grid_remove()
    hidden = not hidden


hidden = False
root = tk.Tk()
e = tk.Entry(root)
e.grid(row=0, column=1)
tk.Button(root, text="Toggle entry", command=toggle_entry).grid(row=0, column=0)
root.mainloop()

# ----------------------------------------------------------
#
# class LukeOutline(tk.Tk):
#
#     #------------------------------------------------------
#     def __init__(self):
#         # Inherit from tk.Tk
#         super().__init__()
#
#         # Title and size of the window
#         self.title('Luke Outline')
#         self.geometry('600x400')
#
#         # Create the drop down menus
#         self.menu = tk.Menu(self,bg='lightgrey',fg='black')
#
#         self.file_menu = tk.Menu(self.menu,tearoff=0,bg='lightgrey',fg='black')
#         self.file_menu.add_command(label='Add Project',command=self.unfinished)
#         self.file_menu.add_command(label='Quit',command=self.quit)
#
#         self.menu.add_cascade(label='File',menu=self.file_menu)
#
#         self.config(menu=self.menu)
#
#         # Create the tabs (Graph, File Explorer, etc.)
#         self.notebook = Notebook(self)
#
#         graph_tab = tk.Frame(self.notebook)
#         file_explorer_tab = tk.Frame(self.notebook)
#
#         # Sets the Graph Tab as a Canvas where figures, images, etc. can be added
#         self.graph_tab = tk.Canvas(graph_tab)
#         self.graph_tab.pack(side=tk.TOP, expand=1)
#
#         # Sets the file explorer tab as a text box (change later)
#         self.file_explorer_tab = tk.Text(file_explorer_tab,bg='white',fg='black')
#         self.file_explorer_tab.pack(side=tk.TOP, expand=1)
#
#         # Add the tabs to the GUI
#         self.notebook.add(graph_tab, text='Graph')
#         self.notebook.add(file_explorer_tab, text='Files')
#
#         self.notebook.pack(fill=tk.BOTH, expand=1)
#
#         # Add the graph to the graph tab
#         self.fig = Figure()
#         graph = FigureCanvasTkAgg(self.fig,self.graph_tab)
#         graph.get_tk_widget().pack(side='top',fill='both',expand=True)
#         EllipseSlider(self.fig)
#
#     #------------------------------------------------------
#     def quit(self):
#         '''
#         Quit the program
#         '''
#         self.destroy()
#
#     #------------------------------------------------------
#     def unfinished(self):
#         '''
#         Messagebox for unfinished items
#         '''
#         msg.showinfo('Unfinished','This feature has not been finished')
#
#     #------------------------------------------------------
#     def random_graph(self):
#         x = list(range(0,10))
#         y = [i**3 for i in x]
#
#         fig = Figure()
#         axes = fig.add_subplot(111)
#         axes.plot(x,y,label=r'$x^3$')
#         axes.legend()
#
#         return fig
#
# #----------------------------------------------------------
#
# class EllipseSlider():
#
#     #------------------------------------------------------
#     def __init__(self,fig):
#         self.fig = fig
#
#         # Initial values
#         self.u = 0.     #x-position of the center
#         self.v = 0.     #y-position of the center
#         self.a = 2.     #radius on the x-axis
#         self.b = 1.5    #radius on the y-axis
#
#         # Points to plot against
#         self.t = np.linspace(0, 2*np.pi, 100)
#
#         # Set up figure with centered axes and grid
#         self.ax = self.fig.add_subplot(111)
#         self.ax.set_aspect(aspect='equal')
#         self.ax.spines['left'].set_position('center')
#         self.ax.spines['bottom'].set_position('center')
#         self.ax.spines['right'].set_color('none')
#         self.ax.spines['top'].set_color('none')
#         self.ax.xaxis.set_ticks_position('bottom')
#         self.ax.yaxis.set_ticks_position('left')
#         self.ax.set_xlim(-2,2)
#         self.ax.set_ylim(-2,2)
#         self.ax.grid(color='lightgray',linestyle='--')
#
#         self.hola = mplcursors.cursor()
#
#         # Initial plot
#         self.l, = self.ax.plot(self.u+self.a*np.cos(self.t),
#             self.v+self.b*np.sin(self.t),'k')
#
#         # Slider setup
#         self.axcolor = 'lightgoldenrodyellow'
#         self.axb = self.fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=self.axcolor)
#         self.axa = self.fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=self.axcolor)
#
#         self.sb = Slider(self.axb, 'Y Radius', 0.1, 2.0, valinit=self.b)
#         self.sa = Slider(self.axa, 'X Radius', 0.1, 2.0, valinit=self.a)
#
#         # Call update as slider is changed
#         self.sb.on_changed(self.update)
#         self.sa.on_changed(self.update)
#
#         # Reset if reset button is pushed
#         self.resetax = self.fig.add_axes([0.8,0.025,0.1,0.04])
#         self.button = Button(self.resetax, 'Reset', color=self.axcolor, hovercolor='0.975')
#
#         self.button.on_clicked(self.reset)
#
#         # Color button setup
#         self.rax = self.fig.add_axes([0.025, 0.5, 0.15, 0.15], facecolor=self.axcolor)
#         self.radio = RadioButtons(self.rax, ('red', 'blue', 'green'), active=0)
#
#         self.radio.on_clicked(self.colorfunc)
#
#
#
#     #------------------------------------------------------
#
#     def update(self, val):
#         '''
#         Updates the plot as sliders are moved
#         '''
#         self.a = self.sa.val
#         self.b = self.sb.val
#         self.l.set_xdata(self.u+self.a*np.cos(self.t))
#         self.l.set_ydata(self.u+self.b*np.sin(self.t))
#
#
#         try:
#             temp = self.hola._selections[0].annotation.get_text()
#             temp_value = temp[temp.find("[")+1:temp.find("]")]
#             print(float(temp_value))
#         except:
#             print('nothing')
#
#     #------------------------------------------------------
#
#     def reset(self, event):
#         '''
#         Resets everything if reset button clicked
#         '''
#         self.sb.reset()
#         self.sa.reset()
#
#     #------------------------------------------------------
#
#     def colorfunc(self, label):
#         '''
#         Changes color of the plot when button clicked
#         '''
#         self.l.set_color(label)
#         self.fig.canvas.draw_idle()
#
# #----------------------------------------------------------
#
# if __name__ == '__main__':
#     luke_gui = LukeOutline()
#     luke_gui.mainloop()

#### Figure for camera

# def animate(i):
#     cam.outputData()
#     # print(cam.data)
#     ax.clear()
#     ax.set_xticks([])
#     ax.set_yticks([])
#
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.spines['left'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#     ax.imshow(cam.data, vmin = globals.vminT, vmax = globals.vmaxT)
#     # print(cam.data)
#     plt.pause(0.0005)
#
#     if cv2.waitKey(1) & keyboard.is_pressed('enter'):
#         cv2.destroyAllWindows()
#         # print('Stop streaming')
#         # libuvc.uvc_stop_streaming(devh)
#
# fig = Figure()
# ax = fig.add_subplot(111)
#
# # fig.tight_layout()
#
# dummy = np.zeros([120, 160])
#
# img = ax.imshow(dummy, interpolation='nearest', vmin = globals.vminT, vmax = globals.vmaxT, animated = True)
# fig.colorbar(img)
#
# current_cmap = plt.cm.get_cmap()
# current_cmap.set_bad(color='black')
#
# cam = TherCam()
# frame_time = 100
#
# ### Window
# win = Tk()
# height = win.winfo_screenheight()
# width = win.winfo_screenwidth()
#
# center = width/2, height/2
#
# win.configure(background = 'black')
# win.attributes('-fullscreen', True)
#
# camera = Frame(win, width=width, height=height)
#
# camera.grid(row=0, column=0, sticky='news')
# camera.grid_propagate(0)
# camera.configure(background = 'black')
#
#
# ### CAMERA MOVE
# label_camera_move = Label(camera, text="Let's find out the temperature of your skin",
#     bg = 'black', fg = 'white', font="none 30 bold", anchor = CENTER)
#
# label_camera_move.place(x= center[0], y=50, anchor="center")
#
# canvas = FigureCanvasTkAgg(fig, master = camera)
# canvas.draw()
# canvas.get_tk_widget().place(x=center[0], y=center[1], anchor="center")
#
# # toolbar = NavigationToolbar2Tk(canvas, camera)
# # toolbar.update()
# # canvas._tkcanvas.grid(row=0, column=0, sticky='news')
#
# cam.startStream()
# ani = animation.FuncAnimation(fig, animate, interval=10, blit=False)
# win.mainloop()


# x = np.random.rand(15)
# y = np.random.rand(15)
# names = np.array(list("ABCDEFGHIJKLMNO"))
# c = np.random.randint(1,5,size=15)
#
# norm = plt.Normalize(1,4)
# cmap = plt.cm.RdYlGn
#
# fig,ax = plt.subplots()
# sc = plt.scatter(x,y,c=c, s=100, cmap=cmap, norm=norm)
#
# annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot.set_visible(False)
#
# def update_annot(ind):
#
#     pos = sc.get_offsets()[ind["ind"][0]]
#     annot.xy = pos
#     text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))),
#                            " ".join([names[n] for n in ind["ind"]]))
#     annot.set_text(text)
#     annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
#     annot.get_bbox_patch().set_alpha(0.4)
#
#
# def hover(event):
#     vis = annot.get_visible()
#     if event.inaxes == ax:
#         cont, ind = sc.contains(event)
#         if cont:
#             update_annot(ind)
#             annot.set_visible(True)
#             fig.canvas.draw_idle()
#         else:
#             if vis:
#                 annot.set_visible(False)
#                 fig.canvas.draw_idle()
#
# fig.canvas.mpl_connect("motion_notify_event", hover)
#
# plt.show()


# Generate data x, y for scatter and an array of images.
# x = np.arange(20)
# y = np.random.rand(len(x))
# arr = np.empty((len(x),10,10))
# for i in range(len(x)):
#     f = np.random.rand(5,5)
#     arr[i, 0:5,0:5] = f
#     arr[i, 5:,0:5] =np.flipud(f)
#     arr[i, 5:,5:] =np.fliplr(np.flipud(f))
#     arr[i, 0:5:,5:] = np.fliplr(f)

# create figure and plot scatter
# fig = plt.figure()
# ax = fig.add_subplot(111)
# line, = ax.plot(x,y, ls="", marker="o")

# create the annotations box

#
# if __name__ == "__main__":
#
#     data = h5py.File('clo8.hdf5', 'r')
#
#     dataK = data['image10'][:120]
#
#     dataC = (dataK - 27315)/100
#
#     fig, ax = plt.subplots(1)
#
#     img = plt.imshow(dataC)
#
#     hola = mplcursors.cursor()
#     while True:
#         plt.pause(0.005)
#
#         try:
#             temp = hola._selections[0].annotation.get_text()
#             temp_value = temp[temp.find("[")+1:temp.find("]")]
#             print(float(temp_value))
#
#         except:
#             continue
#
# string = hola._selections[0].annotation.get_text()
#
# import re
#
# temp = string.split('\n')[2]
# re.split(r"[*]", temp)
#
# temp_value = temp[temp.find("[")+1:temp.find("]")]
#
# float(temp_value)
#
# re.split('\n \n+)', string)
# re.match(r"['(.*)'\]",temp)
# string
# # hola.annotation_positions

# cv2.waitKey(1)
# import matplotlib.pyplot as plt
# import numpy as np
# import mplcursors
#
# data = np.arange(100).reshape((10, 10))
#
# fig, axes = plt.subplots(ncols=2)
# axes[0].imshow(data, interpolation="nearest", origin="lower")
# axes[1].imshow(data, interpolation="nearest", origin="upper",
#                      extent=[200, 300, 400, 500])
# mplcursors.cursor()
#
# fig.suptitle("Click anywhere on the image")
#
# plt.show()
#######################################################
# VIDEO

# cam = TherCam()
# cam.startStream()
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
#
# # fig.tight_layout()
#
# dummy = np.zeros([120, 160])
#
# img = ax.imshow(dummy, interpolation='nearest', vmin = 20, vmax = 40, animated = True)
# fig.colorbar(img)
#
# annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
#                     bbox=dict(boxstyle="round", fc="w"),
#                     arrowprops=dict(arrowstyle="->"))
# annot.set_visible(False)
#
# current_cmap = plt.cm.get_cmap()
# current_cmap.set_bad(color='black')
#
# while True:
#     cam.outputData()
#
#     ax.clear()
#     ax.set_xticks([])
#     ax.set_yticks([])
#
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.spines['left'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#
#     def update_annot(ind):
#
#         pos = img.get_offsets()[ind["ind"][0]]
#         print(pos)
#         annot.xy = pos
#         text = "{}".format(" ".join(list(map(str,ind["ind"]))),
#                                " ".join([names[n] for n in ind["ind"]]))
#         annot.set_text(text)
#         annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
#         annot.get_bbox_patch().set_alpha(0.4)
#     #
#     #
#     def hover(event):
#         vis = annot.get_visible()
#         if event.inaxes == ax:
#             cont, ind = img.contains(event)
#             if cont:
#                 update_annot(ind)
#                 annot.set_visible(True)
#                 fig.canvas.draw_idle()
#             else:
#                 if vis:
#                     annot.set_visible(False)
#                     fig.canvas.draw_idle()
#     # #
#     # #
#     #
#
#
#     img = ax.imshow(cam.data, vmin = 20, vmax = 40)
#     # print(cam.data)
#     fig.canvas.mpl_connect("motion_notify_event", hover)
#
#     plt.pause(0.0005)
#     # plt.show()
#
#     if cv2.waitKey(1) & keyboard.is_pressed('e'):
#         cv2.destroyAllWindows()
#         frame = 1
#         # print('We are done')
#         break


# root = tkinter.Tk()
# root.wm_title("Embedding in Tk")
#
# fig = Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
#
# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#
#
# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)
#
#
# canvas.mpl_connect("key_press_event", on_key_press)
#
#
# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate
#
#
# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)
#
# tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.


# from tkinter import *
# import globals
#
# def raise_frame(frame):
#     frame.tkraise()
#
# ### Window
# win = Tk()
# height = win.winfo_screenheight()
# width = win.winfo_screenwidth()
#
# center = width/2, height/2
#
# win.configure(background = 'black')
# win.attributes('-fullscreen', True)
# # win.geometry('{}x{}+0+0'.format(width, height))
#
# ### Frames to stack
# instructions = Frame(win, width=width, height=height)
#
# instructions.grid(row=0, column=0, sticky='news')
# instructions.grid_propagate(0)
#
#
# ### INSTRUCTIONS
#
# # dummy1 = Label(instructions, text="", bg = 'blue')
#
# label_ins1 = Label(instructions, text="Paste instructions here", bg = 'green', fg = 'white',
#     font = "none 30 bold", anchor = CENTER)
#
# label_ins2 = Label(instructions, text="Paste instructions here", bg = 'yellow', fg = 'black',
#     font = "none 15 bold", anchor = CENTER)
#
# instructions.configure(background = 'yellow')
# # instructions.columnconfigure(0)
# # instructions.rowconfigure(0, weight=1)
#
# # label_ins1.grid(column=1, row=1)
# # label_ins2.grid(column=1, row=1)
#
# label_ins1.place(x=center[0], y=center[1], anchor="center")
# label_ins2.place(x=center[0], y=center[1] + 20, anchor="center")
#
#
# def enterEndIns(event):
#     print(instructions.winfo_width())
#     raise_frame(transition)
#
# instructions.bind('<Return>', enterEndIns)
#
# raise_frame(instructions)
#
# win.mainloop()
