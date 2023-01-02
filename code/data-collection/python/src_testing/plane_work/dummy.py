# # #!/usr/bin/env python3

### To-dos:
# Randomise stuff as Patrick said
# Ensure data saves
# Pressure step: change Z axis according to pressure
# Code training:
    # - label feeling (different temperatures)
    # - do a few trials in all conditions

from tkinter import *
import globals
from dummy_thread import dummy_thread
import threading
import matlab.engine as me

def check(d):
    for k, v in d.items():
        if v[1] == 'on':
            return d[k][0]

frame_time = 200

if __name__ == "__main__":

    win = Tk()
    win.title("Experiment 4")
    height = win.winfo_screenheight()
    width = win.winfo_screenwidth()

    center = width/2, height/2

    win.configure(background = 'black')
    win.attributes('-fullscreen', True)
    #
    for kframe, vframe in globals.frames.items():
        globals.frames[kframe] = [Frame(win, width=width, height=height)]
        globals.frames[kframe].append(('off'))
        globals.frames[kframe][0].grid(row=0, column=0, sticky='news')
        globals.frames[kframe][0].grid_propagate(0)
        globals.frames[kframe][0].focus_set()
        globals.frames[kframe][0].configure(background = 'black')

    def raise_frame(frame):
        global fig
        global animate
        try:
            # print(frame)
            frame.tkraise()
        except:
            pass

        # print('we are trying this')
        if frame == globals.frames['fixation_cross'][0]: # or globals.frames['intro_big_three'][0]:

            if check(globals.frames) == None:
                frame.after(frame_time,lambda:raise_frame(frame))
                # print(check(globals.frames_boolean, frames))
            else:
                # print(frame)
                frame.after(frame_time,lambda:raise_frame(check(globals.frames)))


    def enterEvent(event):
        if globals.frames['response'][1] == 'on':
            if entry_response.get() is None:
                raise_frame(globals.frames['response'][0])
            else:
                globals.answer = entry_response.get()
                globals.frames['response'][1] = 'off'
                raise_frame(globals.frames['fixation_cross'][0])
                entry_response.delete(0, 'end')

    win.bind('<Return>', enterEvent)

    def testValResponse(ans, acttyp):

        if acttyp == '1': #insert
            if ans != 'y' and ans != 'n':
                print(ans)
                return False
        return True


    label_response1 = Label(globals.frames['response'][0], text="Did it feel cold? (y/n)", bg = 'black', fg = 'white',
        font = "none 30 bold", anchor = CENTER)

    label_response2 = Label(globals.frames['response'][0], text="{}".format('\n\n Type your answer \n and press ENTER'), bg = 'black', fg = 'white',
        font = "none 15 bold", anchor = CENTER)

    entry_response = Entry(globals.frames['response'][0], validate = "key")
    entry_response['validatecommand'] = (entry_response.register(testValResponse),'%P','%d')

    label_response1.place(x=center[0], y=center[1], anchor="center")
    label_response2.place(x=center[0] + 350, y=center[1] + 40, anchor="center")
    entry_response.place(x=center[0]+ 300, y=center[1], anchor="center")

    ########################################################################################
    ################################# Fixation cross
    ########################################################################################
    canvas_cross = Canvas(globals.frames['fixation_cross'][0], background = 'black', width = width, height = height, highlightthickness=0)
    canvas_cross.grid(row = 0, column = 0)
    canvas_cross.create_line(center[0], center[1] + 100, center[0], center[1] - 100, fill = 'white', width = 6)
    canvas_cross.create_line(center[0] + 100, center[1], center[0] - 100, center[1], fill = 'white', width = 6)


    ####################### START
    eng = me.start_matlab()
    thread_dummy_exp = threading.Thread(target = dummy_thread, args = [eng], daemon = True)
    thread_dummy_exp.start()

    raise_frame(globals.frames['fixation_cross'][0])

    win.mainloop()

# import time
# import numpy as np
# import matplotlib
# # matplotlib.use("TkAgg")
#
# from camera_dummy import camera_dummy
# import mplcursors
#
# from matplotlib import (
#     backend_tools as tools, cbook, colors, textpath, tight_bbox, transforms,
#     widgets, get_backend, is_interactive, rcParams)
#
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#
# from matplotlib.figure import Figure
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox
#
# import cv2
# from imutils.video import VideoStream
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from matplotlib import animation
#
#
# from classes_colther import Zaber
# from classes_screen import InputScreen
# from classes_camera import TherCam
# import time
# import threading
# import keyboard
#
# # import tkinter as tk                # python 3
# # from tkinter import font  as tkfont # python 3
#
# from tkinter import *
# import globals
# from experiment import experiment
# cursors = tools.cursors
# import matplotlib as mpl
# mpl.rc('image', cmap='hot')
#

#### Figure for camera

# import psychopy.data as psyd
# import numpy as np
#
#
# staircase = psyd.QuestHandler(30, 2, nTrials=60)
#
# # print(staircase._nextIntensity)
#
# responses = np.random.choice([0, 1], size=(100))
#
# staircase.addResponse(1)
# staircase._nextIntensity
#
# counter = 0
# for eachTrial in staircase:
#     staircase.addResponse(responses[counter])
#     # print(staircase._nextIntensity)
#     counter +=1
#
#
# staircase._nextIntensity
#
# staircase.__dict__
#
# staircase.mean()
#
# staircase.mode()
#
# staircase.saveAsText('caca.txt', delim='\t')
#
# import string
#
# staircase.reversalIntensities
#
# string.replace()
#
#
# from psychopy.tools.filetools import openOutputFile, genDelimiter
# genDelimiter('caca.txt')
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
#
#     plt.pause(0.0005)
#
#     if cv2.waitKey(1) & keyboard.is_pressed('enter'):
#         cv2.destroyAllWindows()
#         cam.StopStream()
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
# def enterEvent(event):
#     win.destroy()
#
# win.bind('<Return>', enterEvent)
#
#
# ### CAMERA MOVE
# label_camera_move = Label(camera, text="Let's find out the temperature of your skin",
#     bg = 'black', fg = 'white', font="none 30 bold", anchor = CENTER)
#
# label_camera_move.place(x= center[0], y=50, anchor="center")
#
# label_camera_temp = Label(camera, text="Temp: ",
#     bg = 'black', fg = 'white', font="none 15 ", anchor = CENTER)
#
# label_camera_temp.place(x=center[0], y=100)
#
#     # data= float(arduinoSerialData.readline())
#     #
#     # templabel.config(text=str(data)) #Update label with next text.
#     #
#     # Joes.after(1000, update_label)
#
# canvas = FigureCanvasTkAgg(fig, master = camera)
# canvas.draw()
# canvas.get_tk_widget().place(x=center[0], y=center[1], anchor="center")
#
#
# def mouse_move(event):
#     global label_camera_temp
#
#     if event.inaxes and event.inaxes.get_navigate():
#
#         try:
#             s = event.inaxes.format_coord(event.xdata, event.ydata)
#         except (ValueError, OverflowError):
#             pass
#         else:
#             artists = [a for a in event.inaxes._mouseover_set
#                        if a.contains(event)[0] and a.get_visible()]
#
#             if artists:
#                 a = cbook._topmost_artist(artists)
#                 if a is not event.inaxes.patch:
#                     data = a.get_cursor_data(event)
#                     if data is not None:
#                         data_str = a.format_cursor_data(data)
#                         if data_str is not None:
#                             s = s + ' ' + data_str
#
#                     label_camera_temp.config(text= 'Temp:' + str(data))
#
#     else:
#         pass
#
#
#
#
# canvas.mpl_connect('motion_notify_event', mouse_move)
#
# big_three = Frame(camera, width=100, height=100)
# big_three.grid(row=0, column=0, sticky='news')
# big_three.configure(background = 'black')
# # big_three.place(x=width*0, y=height*0)
#
# instructions_three =    "Controls:\n  - letter 'f' for colther\n  - letter 'h' for camera\n  - letter 'h' for camera\n  - letter 'h' for camera\n  - letter 'h' for camera\n  - letter 'h' for camera\n  - letter 't' for tactile\n  - letter 'c' to close shutter\n  - letter 'o' to open shutter\n  - letter 'h' to home all zabers\n  - press 'enter' to terminate\n  - press arrow 'up' to move x axis forward\n  - press arrow 'down' to move x axis backwards\n  - press arrow 'left' to move y axis forward\n  - press arrow 'right' to move y axis backwards\n  - letter 'd' to move Z axis down\n  - letter 'u' to move Z axis up\n  - letter 'z' to save CONTROL spot position\n  - letter 'x' to save EXPERIMENTAL spot position\n"
#
# label_instructions_three = Label(big_three, text=instructions_three,
#     bg = 'black', fg = 'white', font="none 12", justify=LEFT)
#
# label_instructions_three.pack() #
#
# #
# # Label COLTHER positions
# label_position_colther_experimental = Label(big_three, text="Colther experimental- X:     Y:     Z: ",
#     fg = 'white', font="none 12", justify=LEFT)
#
# label_position_colther_experimental.pack() #place(x=width*0.10, y=height*0.13)
#
# label_position_colther_control = Label(big_three, text="Colther control- X:     Y:     Z: ",
#     bg = 'black', fg = 'white', font="none 12", justify=LEFT)
#
# label_position_colther_control.pack() #place(x=width*0.10, y=height*0.15)
#
#
# # Label TACTILE positions
# label_position_tactile_experimental = Label(big_three, text="Tactile experimental- X:     Y:     Z: ",
#     bg = 'black', fg = 'white', font="none 12", justify=LEFT)
#
# label_position_tactile_experimental.pack() #place(x=width*0.10, y=height*0.18)
#
# label_position_tactile_control = Label(big_three, text="Tactile control- X:     Y:     Z: ",
#     bg = 'black', fg = 'white', font="none 12", justify=LEFT)
#
# label_position_tactile_control.pack() #place(x=width*0.10, y=height*0.20)
#
# # Label CAMERA positions
# label_position_zabering_experimental = Label(big_three, text="Camera experimental- X:     Y:     Z: ",
#     bg = 'black', fg = 'white', font="none 12", justify=LEFT)
#
# label_position_zabering_experimental.pack() #place(x=width*0.10, y=height*0.23)
#
# label_position_zabering_control = Label(big_three, text="Camera control- X:     Y:     Z: ",
#     bg = 'black', fg = 'white', font="none 12", justify=LEFT)
#
# label_position_zabering_control.pack() #place(x=width*0.10, y=height*0.25)
#
# # Bind event to show COLTHER positions
# def showColtherPosExp():
#     if globals.frames['big_three'][1] == 'on':
#         label_position_colther_experimental.config(text= 'Colther experimental-X: ' + str(globals.positions['colther']['experimental'][0]) + 'Y:' + str(globals.positions['colther']['experimental'][1]) + 'Z:' + str(globals.positions['colther']['experimental'][2]))
# win.bind('x', showColtherPosExp)
#
# def showColtherPosCon():
#     if globals.frames['big_three'][1] == 'on':
#         label_position_colther_control.config(text= 'Colther control-X: ' + str(globals.positions['colther']['control'][0]) + 'Y:' + str(globals.positions['colther']['control'][1]) + 'Z:' + str(globals.positions['colther']['control'][2]))
# win.bind('z', showColtherPosCon)
#
# # Bind event to show TACTILE positions
# def showTactilePosExp():
#     if globals.frames['big_three'][1] == 'on':
#         label_position_tactile_experimental.config(text= 'Tactile experimental-X: ' + str(globals.positions['tactile']['experimental'][0]) + 'Y:' + str(globals.positions['tactile']['experimental'][1]) + 'Z:' + str(globals.positions['tactile']['experimental'][2]))
# win.bind('x', showTactilePosExp)
#
# def showTactilePosCon():
#     if globals.frames['big_three'][1] == 'on':
#         label_position_tactile_control.config(text= 'Tactile control-X: ' + str(globals.positions['tactile']['control'][0]) + 'Y:' + str(globals.positions['tactile']['control'][1]) + 'Z:' + str(globals.positions['colther']['control'][2]))
# win.bind('z', showTactilePosCon)
#
# # Bind event to show CAMERA positions
# def showCameraPosExp():
#     if globals.frames['big_three'][1] == 'on':
#         label_position_zabering_experimental.config(text= 'Camera experimental-X: ' + str(globals.positions['camera']['experimental'][0]) + 'Y:' + str(globals.positions['camera']['experimental'][1]) + 'Z:' + str(globals.positions['camera']['experimental'][2]))
# win.bind('x', showCameraPosExp)
#
# def showCameraPosCon():
#     if globals.frames['big_three'][1] == 'on':
#         label_position_zabering_control.config(text= 'Camera control-X: ' + str(globals.positions['camera']['control'][0]) + 'Y:' + str(globals.positions['camera']['control'][1]) + 'Z:' + str(globals.positions['camera']['control'][2]))
# win.bind('z', showCameraPosCon)
#
#
# cam.startStream()
# ani = animation.FuncAnimation(fig, animate, interval=10, blit=False)
# win.mainloop()


#
# def app():
#
#     cam = TherCam()
#     frame_time = 100
#
#     ### Window
#     win = Tk()
#     height = win.winfo_screenheight()
#     width = win.winfo_screenwidth()
#
#     center = width/2, height/2
#
#     win.configure(background = 'black')
#     win.attributes('-fullscreen', True)
#
#     camera = Frame(win, width=width, height=height)
#
#     camera.grid(row=0, column=0, sticky='news')
#     camera.grid_propagate(0)
#     camera.configure(background = 'black')
#
#
#     ### CAMERA MOVE
#     label_camera_move = Label(camera, text="Let's find out the temperature of your skin",
#         bg = 'black', fg = 'white', font="none 30 bold", anchor = CENTER)
#
#     label_camera_move.place(x= center[0], y=50, anchor="center")
#
#     fig = Figure()
#     ax = fig.add_subplot(111)
#
#     # fig.tight_layout()
#
#     dummy = np.zeros([120, 160])
#
#     img = ax.imshow(dummy, interpolation='nearest', vmin = globals.vminT, vmax = globals.vmaxT, animated = True)
#     fig.colorbar(img)
#
#     current_cmap = plt.cm.get_cmap()
#     current_cmap.set_bad(color='black')
#
#     canvas = FigureCanvasTkAgg(fig, master = camera)
#
#     canvas.get_tk_widget().place(x=center[0], y=center[1], anchor="center")
#
#     ############ Start experiment
# #
#     def plotter():
#         while True:
#             cam.outputData()
#             # print(cam.data)
#             # print(cam.data)
#             # img.set_data(data)
#             ax.clear()
#             ax.set_xticks([])
#             ax.set_yticks([])
#
#             ax.spines['top'].set_visible(False)
#             ax.spines['right'].set_visible(False)
#             ax.spines['left'].set_visible(False)
#             ax.spines['bottom'].set_visible(False)
#
#             ax.imshow(cam.data, vmin = globals.vminT, vmax = globals.vmaxT)
#             canvas.draw()
#
#             plt.pause(0.0005)
#
#             # print('we are printing')
#
#     def gui_handler():
#         threading.Thread(target=plotter).start()
#
#     b = Button(camera, text="Start/Stop", command=gui_handler)
#     b.place(x = 50, y = 50)
#
#     cam.startStream()
#     camera.tkraise()
#
#     # thread_experiment = threading.Thread(target = camera_dummy, daemon = True)
#     # thread_experiment.start()
#
#     win.mainloop()
#
# if __name__ == "__main__":
#     app()

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
# import numpy as np
#
# from classes_colther import Zaber
# from classes_screen import InputScreen
# import time
# import threading
# # from classes_screen import ThreadingGUI
#
#
# from tkinter import *              # python 3
# from tkinter import font  as tkfont # python 3
# #import Tkinter as tk     # python 2
# #import tkFont as tkfont  # python 2
#
#
# import globals
# from dummy_thread import dummy_thread
#
#
# def check(d, f):
#     for k, v in d.items():
#         if v == 'on':
#             return f[k]
#
# COUNT=-2
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
# ### Frames to stack
# fixation_cross = Frame(win, width=width, height=height)
# camera_move = Frame(win, width=width, height=height)
# # age = Frame(win, width=width, height=height)
# # instructions = Frame(win, width=width, height=height)
# # break_point = Frame(win, width=width, height=height)
# # break_point_ready = Frame(win, width=width, height=height)
# # response_sensi = Frame(win, width=width, height=height)
# # response_discri = Frame(win, width=width, height=height)
# # transition = Frame(win, width=width, height=height)
# # end = Frame(win, width=width, height=height)
# #
# frames = {'fixation_cross': fixation_cross, 'camera_move': camera_move}
#
#  # 'age': age, 'instructions': instructions, 'break_point': break_point,
#  #            'break_point_ready': break_point_ready, 'response_sensi': response_sensi, 'response_discri': response_discri,
#  #            'transition': transition, 'end': end}
#
# for kframe, vframe in frames.items():
#    vframe.grid(row=0, column=0, sticky='news')
#    vframe.grid_propagate(0)
#
# def raise_frame(frame):
#     try:
#         frame.tkraise()
#     except:
#         pass
#     global frames
#
#     # if frame == transition:
#     #     if check(globals.frames_boolean, frames) == None:
#     #         frame.after(frame_time,lambda:raise_frame(frame))
#     #         print(check(globals.frames_boolean, frames))
#     #     else:
#     #         frame.after(frame_time,lambda:raise_frame(check(globals.frames_boolean, frames)))
#
#     if frame == fixation_cross:
#         if check(globals.frames_boolean, frames) == None:
#             frame.after(frame_time,lambda:raise_frame(frame))
#             print(check(globals.frames_boolean, frames))
#         else:
#             frame.after(frame_time,lambda:raise_frame(check(globals.frames_boolean, frames)))
#
#     # elif frame == break_point:
#     #     if check(globals.frames_boolean, frames) == None:
#     #         frame.after(frame_time,lambda:raise_frame(frame))
#     #         print(check(globals.frames_boolean, frames))
#     #     else:
#     #         frame.after(frame_time,lambda:raise_frame(check(globals.frames_boolean, frames)))
#
#
#     # elif frame == end:
#     #     win.destroy()
#
# ################################################################################
# ######################### Creating screens #####################################
# ################################################################################
#
# ################################# Fixation cross
# canvas = Canvas(fixation_cross, background = 'black', width = width, height = height, highlightthickness=0)
# canvas.grid(row = 0, column = 0)
# canvas.create_line(center[0], center[1] + 100, center[0], center[1] - 100, fill = 'white', width = 6)
# canvas.create_line(center[0] + 100, center[1], center[0] - 100, center[1], fill = 'white', width = 6)
#
# # #################################  CAMERA
#
# label_camera_move = Label(camera_move, text="Let's find out the temperature of your skin",
#     bg = 'black', fg = 'white', font="none 30 bold", anchor = CENTER)
#
# label_camera_move.place(x= center[0], y=10, anchor="center")
#
#
# fig = Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
#
# canvas = FigureCanvasTkAgg(fig, master=camera_move)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().place(x= center[0], y=50, anchor="center")
#
# fig = Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
#
#
# f = Figure(figsize=(5, 5), dpi=(160*120))
# a = f.add_subplot(111)
#
# a.plot([1,2,3,4,5,6,7,8], [2, 6, 1, 8, 4, 2, 1, 5])
#
# canvas = FigureCanvasTkAgg(f, master = win)
# canvas.show()
# canvas.get_tk_widget().place(x=center[0], y=center[1], anchor="center")

# #################################  AGE
# def testValAge(ans, acttyp):
#
#     if acttyp == '1': #insert
#         try:
#             inte = int(ans)
#             return True
#         except:
#             return False
#
#     return True
#
#
# label_age1 = Label(age, text="How old are you?", bg = 'black', fg = 'white',
#     font = "none 30 bold")
#
# label_age2 = Label(age, text="{}".format('\n\n Click on the box, type your answer \n and press enter'), bg = 'black', fg = 'white',
#     font = "none 15 bold")
#
# entry_age = Entry(age, validate = "key")
# entry_age['validatecommand'] = (entry_age.register(testValAge),'%P','%d')
#
# age.configure(background = 'black')
#
# label_age1.place(x=center[0] - 40, y=center[1], anchor="center")
# entry_age.place(x=center[0], y=center[1], anchor="center")
# label_age2.place(x=center[0] + 40, y=center[1] + 40, anchor="center")
#
# def enterEndAge(event):
#     globals.subj_age = entry_age.get()
#     raise_frame(transition)
#     print(globals.subj_age)
#
# age.bind('<Return>', enterEndAge)
#
# ### INSTRUCTIONS
#
# # dummy1 = Label(instructions, text="", bg = 'blue')
#
# label_ins1 = Label(instructions, text="Paste instructions here", bg = 'black', fg = 'white',
#     font = "none 30 bold", anchor = CENTER)
#
# label_ins2 = Label(instructions, text="Press enter when you are ready to continue", bg = 'black', fg = 'white',
#     font = "none 15 bold", anchor = CENTER)
#
# instructions.configure(background = 'black')
#
# label_ins1.place(x=center[0], y=center[1], anchor="center")
# label_ins2.place(x=center[0] + 40, y=center[1] + 40, anchor="center")
#
#
# def enterEndIns(event):
#     print('we are here')
#     raise_frame(transition)
#
# instructions.bind('<Return>', enterEndIns)
#
# ### BREAK POINT
#
# break_point1 = Label(break_point, text="Let's take a short break", bg = 'black', fg = 'white',
#     font = "none 30 bold", anchor = CENTER)
#
# break_point.configure(background = 'black')
#
# break_point1.place(x=center[0], y=center[1], anchor="center")
#
# ### BREAK POINT READY
#
# break_point_ready1 = Label(break_point_ready, text=" Press enter when you are ready to continue", bg = 'black', fg = 'white',
#     font = "none 30 bold", anchor = CENTER)
#
# break_point_ready.configure(background = 'black')
#
# break_point_ready.place(x=center[0], y=center[1], anchor="center")
#
# def enterEndBreTrans(event):
#     raise_frame(transition)
#
# break_point_ready.bind('<Return>', enterEndBreTrans)
#
# ### RESPONSE SENSITIVITY
# def testValSensi(ans, acttyp):
#
#     if acttyp == '1': #insert
#         if ans != 'y' & ans != 'n':
#             return False
#
#     return True
#
#
# label_sensi1 = Label(response_sensi, text="Did you feel anything?", bg = 'black', fg = 'white',
#     font = "none 30 bold", anchor = CENTER)
#
# label_sensi2 = Label(response_sensi, text="{}".format('\n\n Click on the box, type your answer \n and press enter'), bg = 'black', fg = 'white',
#     font = "none 15 bold", anchor = CENTER)
#
#
# entry_sensi = Entry(response_sensi, validate = "key")
# entry_sensi['validatecommand'] = (entry_sensi.register(testValSensi),'%P','%d')
#
# response_sensi.configure(background = 'black')
#
# label_sensi1.place(x=center[0] - 100, y=center[1], anchor="center")
# label_sensi2.place(x=center[0], y=center[1], anchor="center")
# entry_sensi.place(x=center[0]+ 40, y=center[1] + 40, anchor="center")
#
#
# def enterEndSensi(event):
#     globals.sensi_response = entry_sensi.get()
#     raise_frame(transition)
#
# response_sensi.bind('<Return>', enterEndSensi)
#
# ### RESPONSE DISCRIMINATION
# def testValSensi(ans, acttyp):
#
#     if acttyp == '1': #insert
#         if ans != 'y' & ans != 'n':
#             return False
#
#     return True
#
#
# label_discri1 = Label(response_discri, text="Did it feel cold? (y/n)", bg = 'black', fg = 'white',
#     font = "none 30 bold", anchor = CENTER)
#
# label_discri2 = Label(response_discri, text="{}".format('\n\n Click on the box, type your answer \n and press enter'), bg = 'black', fg = 'white',
#     font = "none 15 bold", anchor = CENTER)
#
#
# entry_discri = Entry(response_discri, validate = "key")
# entry_discri['validatecommand'] = (entry_discri.register(testValSensi),'%P','%d')
#
# response_discri.configure(background = 'black')
#
# label_discri1.place(x=center[0] - 100, y=center[1], anchor="center")
# label_discri2.place(x=center[0], y=center[1], anchor="center")
# entry_discri.place(x=center[0]+ 40, y=center[1] + 40, anchor="center")
#
#
# def enterEndDiscri(event):
#     globals.discri_response = entry_discri.get()
#     raise_frame(transition)
#
# response_discri.bind('<Return>', enterEndDiscri)
#
# ### TRANSITION
#
# transition.configure(background = 'black')
#
# ### END
# label_end1 = Label(end, text="We are done!", bg = 'black', fg = 'white',
#     font = "none 30 bold", anchor = CENTER)
#
# label_end2 = Label(end, text="{}".format('\n\n Press enter to finish the Experiment'), bg = 'black', fg = 'white',
#     font = "none 15 bold", anchor = CENTER)
#
# end.configure(background = 'black')
#
# label_end1.place(x=center[0], y=center[1], anchor="center")
# label_end2.place(x=center[0]+40, y=center[1]-40, anchor="center")



############ Start experiment

# threaddummy = threading.Thread(target = dummy_thread, daemon = True)



# class SampleApp(tk.Tk):
#
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#
#         # win = tk.Tk()
#         #
#         # win.configure(background = 'black')
#         # win.attributes('-fullscreen', True)
#
#         # the container is where we'll stack a bunch of frames
#         # on top of each other, then the one we want visible
#         # will be raised above the others
#         container = tk.Frame(self)
#         container.attributes('-fullscreen', True)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#
#         self.frames = {}
#         for F in (StartPage, PageOne, PageTwo):
#             page_name = F.__name__
#             frame = F(parent=container, controller=self)
#             self.frames[page_name] = frame
#
#             # put all of the pages in the same location;
#             # the one on the top of the stacking order
#             # will be the one that is visible.
#             frame.grid(row=0, column=0, sticky="nsew")
#
#         self.show_frame("StartPage")
#
#     def show_frame(self, page_name):
#         '''Show a frame for the given page name'''
#         frame = self.frames[page_name]
#         frame.tkraise()
#
#
# class StartPage(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#
#         self.controller = controller
#         label = tk.Label(self, text="This is the start page")
#         label.pack(side="top", fill="x", pady=10)
#
#         button1 = tk.Button(self, text="Go to Page One",
#                             command=lambda: controller.show_frame("PageOne"))
#         button2 = tk.Button(self, text="Go to Page Two",
#                             command=lambda: controller.show_frame("PageTwo"))
#         button1.pack()
#         button2.pack()
#
#
# class PageOne(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#
#         self.controller = controller
#         label = tk.Label(self, text="This is page 1")
#         label.pack(side="top", fill="x", pady=10)
#         button = tk.Button(self, text="Go to the start page",
#                            command=lambda: controller.show_frame("StartPage"))
#         button.pack()
#
#
# class PageTwo(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#
#         self.controller = controller
#         label = tk.Label(self, text="This is page 2")
#         label.pack(side="top", fill="x", pady=10)
#         button = tk.Button(self, text="Go to the start page",
#                            command=lambda: controller.show_frame("StartPage"))
#         button.pack()
#
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()


#
# class SampleApp(tk.Tk):
#
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         win = tk.Tk()
#
#         win.configure(background = 'black')
#         win.attributes('-fullscreen', True)
#
#         # the container is where we'll stack a bunch of frames
#         # on top of each other, then the one we want visible
#         # will be raised above the others
#         container = tk.Frame(win)
#
#         container.pack(side="top", fill="both", expand=True)
#         # container.grid_rowconfigure(0, weight=1)
#         # container.grid_columnconfigure(0, weight=1)
#
#         self.frames = {}
#         for F in (StartPage, PageOne, PageTwo):
#             page_name = F.__name__
#             frame = F(win=win, parent=container, controller=self)
#             self.frames[page_name] = frame
#             print(frame)
#
#             # put all of the pages in the same location;
#             # the one on the top of the stacking order
#             # will be the one that is visible.
#             # frame.grid(row=0, column=0, sticky="nsew")
#
#         self.show_frame("StartPage")
#
#     def show_frame(self, page_name):
#         '''Show a frame for the given page name'''
#         frame = self.frames[page_name]
#         frame.tkraise()
#
#
#
# def StartPage(win, parent, controller):
#     start_frame = tk.Frame(win, parent)
#     label = tk.Label(start_frame)
#     label.pack(side="top", fill="x", pady=10)
#
#     button1 = tk.Button(start_frame, text="Go to Page One",
#                         command=lambda: controller.show_frame("PageOne"))
#     button2 = tk.Button(start_frame, text="Go to Page Two",
#                         command=lambda: controller.show_frame("PageTwo"))
#     button1.pack()
#     button2.pack()
#
#     return start_frame
#
#
#
# def PageOne(win, parent, controller):
#     one_frame = tk.Frame(win, parent)
#     label = tk.Label(one_frame)
#     label.pack(side="top", fill="x", pady=10)
#     button = tk.Button(one_frame, text="Go to the start page",
#                        command=lambda: controller.show_frame("StartPage"))
#     button.pack()
#
#     return one_frame
#
#
#
# def PageTwo(win, parent, controller):
#     two_frame = tk.Frame(win, parent)
#     label = tk.Label(two_frame)
#     label.pack(side="top", fill="x", pady=10)
#     button = tk.Button(two_frame, text="Go to the start page",
#                        command=lambda: controller.show_frame("StartPage"))
#     button.pack()
#
#     return two_frame
#
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()

# hola = InputScreen('How old are you?  \n Click on the box, type your answer and press enter')
#
# print(type(hola.input))


# from tkinter import Tk, Canvas, Frame, BOTH


# class Example():
#
#     def __init__(self):
#         win = tk.Tk()
#
#         # win.attributes('-fullscreen', True)
#         win.configure(background = 'black')
#         value = win.winfo_screenwidth
#         print(value)
#         print(win.winfo_screenheight)
#
#         canvas = Canvas(win, background = 'black', highlightthickness=0)
#         canvas.grid(row = 0, column = 0)
#         canvas.create_line(0, 0, 400, 400, fill = 'white')
#
#         x0 = win.winfo_reqwidth()
#         print(x0)
#
#         win.mainloop()
#
#
#
# def main():

    # ex = Example()

#
# from tkinter import *
# from tkinter.ttk import *
# #
# # # creating tkinter window
# win = Tk()
#
# # getting screen's height in pixels
# win.attributes('-fullscreen', True)
# win.configure(background = 'black')
#
# # getting screen's width in pixels
# height = win.winfo_screenheight()
# width = win.winfo_screenwidth()
#
# center = width/2, height/2
#
# canvas = Canvas(win, background = 'black', width = width, height = height, highlightthickness=0)
# canvas.grid(row = 0, column = 0)
# canvas.create_line(center[0], center[1] + 100, center[0], center[1] - 100, fill = 'white', width = 6)
# canvas.create_line(center[0] + 100, center[1], center[0] - 100, center[1], fill = 'white', width = 6)
#
# # infinite loop
#
#
# win.mainloop()






# from tkinter import *
#
#
# def raise_frame(frame):
#     frame.tkraise()
#
# root = Tk()
#
# f1 = Frame(root)
# f2 = Frame(root)
# f3 = Frame(root)
# f4 = Frame(root)
#
# for frame in (f1, f2, f3, f4):
#     frame.grid(row=0, column=0, sticky='news')
#
# Button(f1, text='Go to frame 2', command=lambda:raise_frame(f2)).pack()
# Label(f1, text='FRAME 1').pack()
#
# Label(f2, text='FRAME 2').pack()
# Button(f2, text='Go to frame 3', command=lambda:raise_frame(f3)).pack()
#
# Label(f3, text='FRAME 3').pack(side='left')
# Button(f3, text='Go to frame 4', command=lambda:raise_frame(f4)).pack(side='left')
#
# Label(f4, text='FRAME 4').pack()
# Button(f4, text='Goto to frame 1', command=lambda:raise_frame(f1)).pack()
#
# raise_frame(f1)
# root.mainloop()
