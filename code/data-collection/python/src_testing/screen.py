import numpy as np
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import cv2
from imutils.video import VideoStream
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import matlab.engine as me

from classes_colther import Zaber
from classes_screen import InputScreen
from classes_camera import TherCam
import time
import threading
import keyboard

from matplotlib import (
    backend_tools as tools, cbook, colors, textpath, tight_bbox, transforms,
    widgets, get_backend, is_interactive, rcParams)

cursors = tools.cursors

from tkinter import *
import globals
from experiment import experiment

from queue import Queue

def check(d):
    for k, v in d.items():
        if v[1] == 'on':
            return d[k][0]

#### Figure for camera

import matplotlib as mpl
mpl.rc('image', cmap='hot')

# We use an animation to plot matplotlib thermal camera plot within a tkinter window.
# We need to do tkinter and matplotlib in main thread. So, we call the thermal camera object
# in the experiment thread as a global variable and then we can use data in main thread
# while we control camera with experiment thread

def animate_zabering(i):
    if globals.ani_boolean == False:
        # print('no CAMERA')
        pass
    if globals.ani_boolean == True:

        globals.cam.outputData()
        # print(globals.cam.data)

        ax_zabering.clear()
        ax_zabering.set_xticks([])
        ax_zabering.set_yticks([])

        ax_zabering.spines['top'].set_visible(False)
        ax_zabering.spines['right'].set_visible(False)
        ax_zabering.spines['left'].set_visible(False)
        ax_zabering.spines['bottom'].set_visible(False)
        ax_zabering.imshow(globals.cam.data, vmin = globals.vminT, vmax = globals.vmaxT)

        if not globals.hidden:
            ax_zabering.add_artist(globals.cam.circles[0])

        plt.pause(0.0005)

        if cv2.waitKey(1) & keyboard.is_pressed('enter'):
            cv2.destroyAllWindows()


dummy = np.zeros([120, 160])

# Finding skin temperature
fig_zabering = Figure()
ax_zabering = fig_zabering.add_subplot(111)

img_zabering = ax_zabering.imshow(dummy, interpolation='nearest', vmin = globals.vminT, vmax = globals.vmaxT, animated = True)
fig_zabering.colorbar(img_zabering)


if __name__ == "__main__":

    frame_time = 100

    ### Window
    win = Tk()
    win.title("Experiment 4")
    height = win.winfo_screenheight()
    width = win.winfo_screenwidth()

    center = width/2, height/2

    win.configure(background = 'black')
    win.attributes('-fullscreen', True)

    ### Frames to stack. We create a dictionary for the frames that we are going to use throughout the experiment

    ### We create the frames and we set settings so we can easily place widgets on them
    for kframe, vframe in globals.frames.items():
        globals.frames[kframe] = [Frame(win, width=width, height=height, name='{}'.format(kframe))]
        globals.frames[kframe].append(('off'))
        globals.frames[kframe][0].grid(row=0, column=0, sticky='news')
        globals.frames[kframe][0].grid_propagate(0)
        globals.frames[kframe][0].focus_set()
        globals.frames[kframe][0].configure(background = 'black')

    ### This function moves forward the frame which global variable is set to on
    def raise_frame(frame):
        global fig
        global animate
        # The frame that we call below is raised in here
        try:
            # print(frame)
            frame.tkraise()
        except:
            pass

        # print(globals.frames['n_participant'][0])

        # Basically frames that don't have special stuff for their widgets are called with a delay until boolean changes
        # frames that require special stuff for their widgets are set up separately
        try:
            if frame == globals.frames['transition'][0] or frame == globals.frames['fixation_cross'][0] or frame == globals.frames['break_point'][0] or frame == globals.frames['start'][0] or frame == globals.frames['intro_big_three'][0] or frame == globals.frames['intro_training'][0] or frame == globals.frames['intro_trials'][0] or frame == globals.frames['intro_tactile_height'][0]:

                if check(globals.frames) == None:
                    frame.after(frame_time,lambda:raise_frame(frame)) #

                else:
                    frame.after(frame_time,lambda:raise_frame(check(globals.frames))) #frame.after(frame_time,lambda:

            elif frame == globals.frames['n_participant'][0]:
                entry_parti.focus_set()

            elif frame == globals.frames['age'][0]:
                entry_age.focus_set()

            elif frame == globals.frames['response'][0]:
                entry_response.focus_set()

            elif frame == globals.frames['baseline_temp'][0]:
                entry_response.focus_set()

            elif frame == globals.frames['zabering'][0]:
                globals.ani_boolean = True

                # this is here cos we can only use animate and frame, so whatever frame we create to display thermal camera
                # we need to reuse it, we show and hide stuff depending on the experiment stage

                if globals.hidden:
                    big_three.grid_remove()
                else:
                    big_three.grid()

            # elif frame == globals.frames['tactile_height'][0]:
            #     dummy = 0

            elif frame == globals.frames['repeat_training'][0]:
                entry_response.focus_set()

        except:
            print('we failed to try')
            # frame.after(frame_time,lambda:raise_frame(globals.frames['transition'][0]))
            pass

    def enterEvent(event):
        if globals.frames['n_participant'][1] == 'on':
            globals.n_subj = entry_parti.get()
            globals.frames['n_participant'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['response'][1] == 'on':
            if entry_response.get() is None:
                raise_frame(globals.frames['response'][0])
            else:
                globals.answer = entry_response.get()
                globals.frames['response'][1] = 'off'
                raise_frame(globals.frames['fixation_cross'][0])
                entry_response.delete(0, 'end')

        elif globals.frames['break_point_ready'][1] == 'on':
            globals.frames['break_point_ready'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['baseline_temp'][1] == 'on':
            globals.baseline_temp = entry_base_temp.get()
            globals.frames['baseline_temp'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['instructions'][1] == 'on':
            globals.frames['instructions'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['age'][1] == 'on':
            globals.subj_age = entry_age.get()
            globals.frames['age'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['microspots'][1] == 'on':
            globals.frames['microspots'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['zabering'][1] == 'on':
            globals.frames['zabering'][1] = 'off'
            raise_frame(globals.frames['transition'][0])
            globals.ani_boolean = False

        elif globals.frames['intro_big_three'][1] == 'on':
            globals.frames['intro_big_three'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['intro_training'][1] == 'on':
            globals.frames['intro_training'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['repeat_training'][1] == 'on':
            globals.training_boolean = entry_response.get()
            globals.frames['repeat_training'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['intro_trials'][1] == 'on':
            globals.frames['intro_trials'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['tactile_height'][1] == 'on':
            globals.frames['tactile_height'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['intro_tactile_height'][1] == 'on':
            globals.frames['intro_tactile_height'][1] = 'off'
            raise_frame(globals.frames['transition'][0])

        elif globals.frames['end'][1] == 'on':
            globals.frames['end'][1] = 'off'
            win.destroy()

    win.bind('<Return>', enterEvent)

    ################################################################################
    ######################### Creating screens #####################################
    ################################################################################

    ########################################################################################
    ################################# Fixation cross
    ########################################################################################
    canvas_cross = Canvas(globals.frames['fixation_cross'][0], background = 'black', width = width, height = height, highlightthickness=0)
    canvas_cross.grid(row = 0, column = 0)
    canvas_cross.create_line(center[0], center[1] + 100, center[0], center[1] - 100, fill = 'white', width = 6)
    canvas_cross.create_line(center[0] + 100, center[1], center[0] - 100, center[1], fill = 'white', width = 6)

    ########################################################################################
    #################################  AGE
    ########################################################################################

    def testValAge(ans, acttyp):

        if acttyp == '1': #insert
            try:
                inte = int(ans)
                return True
            except:
                return False

        return True

    label_age1 = Label(globals.frames['age'][0], text="How old are you?", bg = 'black', fg = 'white',
        font = "none 30 bold")

    label_age2 = Label(globals.frames['age'][0], text="{}".format('\n\n Type your answer \n and press ENTER'), bg = 'black', fg = 'white',
        font = "none 15 bold")

    entry_age = Entry(globals.frames['age'][0], validate = "key")
    entry_age['validatecommand'] = (entry_age.register(testValAge),'%P','%d')

    label_age1.place(x=center[0] - 250, y=center[1], anchor="center")
    entry_age.place(x=center[0], y=center[1], anchor="center")
    label_age2.place(x=center[0] + 40, y=center[1] + 40, anchor="center")

    ########################################################################################
    #################################  Number participant
    ########################################################################################
    def testValParti(ans, acttyp):

        if acttyp == '1': #insert
            try:
                inte = int(ans)
                return True
            except:
                return False

        return True


    label_parti1 = Label(globals.frames['n_participant'][0], text="Participant number: ", bg = 'black', fg = 'white',
        font = "none 30 bold")

    label_parti2 = Label(globals.frames['n_participant'][0], text="{}".format('\n\n Type your answer \n and press ENTER'), bg = 'black', fg = 'white',
        font = "none 15 bold")

    entry_parti = Entry(globals.frames['n_participant'][0], validate = "key")
    entry_parti['validatecommand'] = (entry_parti.register(testValParti),'%P','%d')
    # entry_parti.focus_set()

    label_parti1.place(x=center[0] - 250, y=center[1], anchor="center")
    entry_parti.place(x=center[0], y=center[1], anchor="center")
    label_parti2.place(x=center[0] + 40, y=center[1] + 40, anchor="center")

    ########################################################################################
    ### INSTRUCTIONS
    ########################################################################################

    label_ins1 = Label(globals.frames['instructions'][0], text="Paste instructions here", bg = 'black', fg = 'white',
        font = "none 30 bold", anchor = CENTER)

    label_ins2 = Label(globals.frames['instructions'][0], text="Press enter when you are ready to continue", bg = 'black', fg = 'white',
        font = "none 15 bold", anchor = CENTER)

    label_ins1.place(x=center[0], y=center[1], anchor="center")
    label_ins2.place(x=center[0] + 40, y=center[1] + 40, anchor="center")
    ########################################################################################
    ### BREAK POINT
    ########################################################################################

    break_point1 = Label(globals.frames['break_point'][0], text="Let's take a short break", bg = 'black', fg = 'white',
        font = "none 30 bold", anchor = CENTER)

    break_point1.place(x=center[0], y=center[1], anchor="center")

    ########################################################################################
    ### BREAK POINT READY
    ########################################################################################

    break_point_ready1 = Label(globals.frames['break_point_ready'][0], text=" Press enter when you are ready to continue", bg = 'black', fg = 'white',
        font = "none 30 bold", anchor = CENTER)

    break_point_ready1.place(x=center[0], y=center[1], anchor="center")


    ########################################################################################
    ### TRANSITION
    ########################################################################################

    ########################################################################################
    ### RESPONSE
    ########################################################################################

    def testValResponse(ans, acttyp):

        if acttyp == '1': #insert
            if ans != 'a' and ans != 's':
                # print(ans)
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
    ### END
    ########################################################################################

    label_end1 = Label(globals.frames['end'][0], text="We are done!", bg = 'black', fg = 'white',
        font = "none 30 bold", anchor = CENTER)
    label_end2 = Label(globals.frames['end'][0], text="Press enter to finish the experiment", bg = 'black', fg = 'white',
        font = "none 15 bold", anchor = CENTER)

    label_end1.place(x=center[0], y=center[1], anchor="center")
    label_end2.place(x=center[0] + 40, y=center[1] + 60, anchor="center")

    ########################################################################################
    ### START
    ########################################################################################

    label_start1 = Label(globals.frames['start'][0], text="Thanks for coming. We are about to start the experiment", bg = 'black', fg = 'white',
        font = "none 30 bold", anchor = CENTER)

    label_start1.place(x=center[0], y=center[1], anchor="center")

    ########################################################################################
    ### MICROSPOTS
    ########################################################################################

    label_microspots1 = Label(globals.frames['microspots'][0], text="First, we are going to find spots that are \n sensitive to cold stimulations",
        bg = 'black', fg = 'white', font = "none 30 bold", anchor = CENTER)

    label_microspots1.place(x=center[0], y=center[1], anchor="center")

    ########################################################################################
    ### BASELINE TEMPERATURE
    ########################################################################################

    def testValBase(ans, acttyp):
        if acttyp == '1': #insert
         try:
             inte = int(ans)
             return True
         except:
             return False

        return True


    label_base1 = Label(globals.frames['baseline_temp'][0], text="What is the baseline temperature? ", bg = 'black', fg = 'white', font = "none 30 bold")

    label_base2 = Label(globals.frames['baseline_temp'][0], text="{}".format('\n\n Type your answer \n and press ENTER'), bg = 'black', fg = 'white',
         font = "none 15 bold")

    entry_base_temp = Entry(globals.frames['baseline_temp'][0], validate = "key")
    entry_base_temp['validatecommand'] = (entry_parti.register(testValBase),'%P','%d')
     # entry_parti.focus_set()

    label_base1.place(x=center[0] - 250, y=center[1], anchor="center")
    entry_base_temp.place(x=center[0] + 100, y=center[1], anchor="center")
    label_base2.place(x=center[0] + 140, y=center[1] + 40, anchor="center")

    ########################################################################################
    ### ZABERING
    ########################################################################################

    def testValSteps(ans, acttyp):

        if acttyp == '1': #insert
            try:
                inte = int(ans)
                return True
            except:
                return False

        return True

    # label_zabering = Label(globals.frames['zabering'][0], text="Let's find out the temperature of your skin",
    #     bg = 'black', fg = 'white', font="none 30 bold", anchor = CENTER)
    #
    # label_zabering.place(x= center[0], y=50, anchor="center")

    canvas_zabering = FigureCanvasTkAgg(fig_zabering, master = globals.frames['zabering'][0])
    canvas_zabering.draw()
    canvas_zabering.get_tk_widget().place(x=center[0], y=center[1], anchor="center")

    label_zaber_steps = Label(globals.frames['zabering'][0], text="How much would you like the Zaber to move?",
        bg = 'black', fg = 'white', font="none 15", anchor = CENTER)

    label_zaber_steps.place(x= center[0] + 400, y=center[1] + 370, anchor="center")

    entry_zaber_steps = Entry(globals.frames['zabering'][0], validate = "key")
    entry_zaber_steps.place(x= center[0] + 400, y=center[1] + 400, anchor="center")

    entry_zaber_steps['validatecommand'] = (entry_zaber_steps.register(testValSteps),'%P','%d')

    def onSteps():
        globals.amount = int(entry_zaber_steps.get())
        entry_zaber_steps.delete(0, 'end')

    button_zaber_steps = Button(globals.frames['zabering'][0], text="Update steps", command=onSteps,
        bg = 'green', fg = 'black', font="none 15", anchor = CENTER)

    button_zaber_steps.place(x= center[0] + 600, y=center[1] + 400, anchor="center")

    label_zabering_temp = Label(globals.frames['zabering'][0], text="Temp: ",
        bg = 'black', fg = 'white', font="none 15 ", anchor = CENTER)

    label_zabering_temp.place(x=width*0.90, y=height*0.2)

    def mouse_move(event):
        global label_zabering_temp

        if event.inaxes and event.inaxes.get_navigate():

            try:
                s = event.inaxes.format_coord(event.xdata, event.ydata)
            except (ValueError, OverflowError):
                pass
            else:
                artists = [a for a in event.inaxes._mouseover_set
                           if a.contains(event)[0] and a.get_visible()]

                if artists:
                    a = cbook._topmost_artist(artists)
                    if a is not event.inaxes.patch:
                        data = a.get_cursor_data(event)
                        if data is not None:
                            data_str = a.format_cursor_data(data)
                            if data_str is not None:
                                s = s + ' ' + data_str

                        label_zabering_temp.config(text= 'Temp: ' + str(data))

        else:
            pass

    canvas_zabering.mpl_connect('motion_notify_event', mouse_move)

    big_three = Frame(globals.frames['zabering'][0], width=100, height=100)
    big_three.grid(row=0, column=0, sticky='news')
    big_three.configure(background = 'black')
    # big_three.place(x=width*0, y=height*0)

    instructions_three =    "Controls:\n  - letter 'f' for COLTHER\n  - letter 'k' for CAMERA\n - letter 't' for TACTILE\n - letter 'n' for NON-TACTILE\n\n  - letter 'c' to close shutter\n  - letter 'o' to open shutter\n\n - press arrow 'up' to move x axis forward\n  - press arrow 'down' to move x axis backwards\n  - press arrow 'left' to move y axis forward\n  - press arrow 'right' to move y axis backwards\n  - letter 'd' to move Z axis down\n  - letter 'u' to move Z axis up\n\n  - letter 'z' to save CONTROL spot position\n  - letter 'x' to save EXPERIMENTAL spot position\n\n - letter 'p' to save ROI coordinates CONTRORL \n - letter 'i' to save ROI coordinates EXPERIMENTAL \n\n - letter 'h' to home all zabers\n  - press 'enter' to terminate\n"

    label_instructions_three = Label(big_three, text=instructions_three,
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_instructions_three.pack() #

    #
    # Label COLTHER positions
    label_position_colther_experimental = Label(big_three, text="Colther experimental- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_colther_experimental.pack() #place(x=width*0.10, y=height*0.13)

    label_position_colther_control = Label(big_three, text="Colther control- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_colther_control.pack() #place(x=width*0.10, y=height*0.15)


     # Label TACTILE positions
    label_position_tactile_experimental = Label(big_three, text="Tactile experimental- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_tactile_experimental.pack() #place(x=width*0.10, y=height*0.18)

    label_position_tactile_control = Label(big_three, text="Tactile control- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_tactile_control.pack() #place(x=width*0.10, y=height*0.20)

    # Label NON-TACTILE positions
    label_position_non_tactile_experimental = Label(big_three, text="Non-tactile experimental- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_non_tactile_experimental.pack() #place(x=width*0.10, y=height*0.18)

    label_position_non_tactile_control = Label(big_three, text="Non-tactile control- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_non_tactile_control.pack() #place(x=width*0.10, y=height*0.20)

    # Label CAMERA positions
    label_position_zabering_experimental = Label(big_three, text="Camera experimental- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_zabering_experimental.pack() #place(x=width*0.10, y=height*0.23)

    label_position_zabering_control = Label(big_three, text="Camera control- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_zabering_control.pack() #place(x=width*0.10, y=height*0.25)

    # Label ROI positions

    label_ROI_experimental = Label(big_three, text="ROI experimental- X:     Y: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_ROI_experimental.pack() #place(x=width*0.10, y=height*0.23)

    label_ROI_control = Label(big_three, text="ROI control- X:     Y: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_ROI_control.pack() #place(x=width*0.10, y=height*0.25)

    # Bind event to show COLTHER positions
    def showPosExp(event):
        if globals.frames['zabering'][1] == 'on':
            if globals.current_device == 'colther':
                label_position_colther_experimental.config(text= 'Colther experimental-X: ' + str(globals.positions['colther']['experimental'][0]) + ' Y: ' + str(globals.positions['colther']['experimental'][1]) + ' Z: ' + str(globals.positions['colther']['experimental'][2]))

            elif globals.current_device == 'non_tactile':
                label_position_non_tactile_experimental.config(text= 'Non-tactile experimental-X: ' + str(globals.positions['non_tactile']['experimental'][0]) + ' Y: ' + str(globals.positions['non_tactile']['experimental'][1]) + ' Z: ' + str(globals.positions['non_tactile']['experimental'][2]))

            elif globals.current_device == 'tactile':
                label_position_tactile_experimental.config(text= 'Tactile experimental-X: ' + str(globals.positions['tactile']['experimental'][0]) + ' Y: ' + str(globals.positions['tactile']['experimental'][1]) + ' Z: ' + str(globals.positions['tactile']['experimental'][2]))

            elif globals.current_device == 'camera':
                label_position_zabering_experimental.config(text= 'Camera experimental-X: ' + str(globals.positions['camera']['experimental'][0]) + ' Y: ' + str(globals.positions['camera']['experimental'][1]) + ' Z: ' + str(globals.positions['camera']['experimental'][2]))

    win.bind('x', showPosExp)

    def showPosCon(event):
        if globals.frames['zabering'][1] == 'on':
            if globals.current_device == 'colther':
                label_position_colther_control.config(text= 'Colther control-X: ' + str(globals.positions['colther']['control'][0]) + ' Y: ' + str(globals.positions['colther']['control'][1]) + ' Z: ' + str(globals.positions['colther']['control'][2]))

            elif globals.current_device == 'tactile':
                label_position_tactile_control.config(text= 'Tactile control-X: ' + str(globals.positions['tactile']['control'][0]) + ' Y: ' + str(globals.positions['tactile']['control'][1]) + ' Z: ' + str(globals.positions['tactile']['control'][2]))

            elif globals.current_device == 'non_tactile':
                label_position_non_tactile_control.config(text= 'Non-tactile control-X: ' + str(globals.positions['non_tactile']['control'][0]) + ' Y: ' + str(globals.positions['non_tactile']['control'][1]) + ' Z: ' + str(globals.positions['non_tactile']['control'][2]))

            elif globals.current_device == 'camera':
                label_position_zabering_control.config(text= 'Camera control-X: ' + str(globals.positions['camera']['control'][0]) + ' Y: ' + str(globals.positions['camera']['control'][1]) + ' Z: ' + str(globals.positions['camera']['control'][2]))

    win.bind('z', showPosCon)

    def showROICcontrol(event):
        if globals.frames['zabering'][1] == 'on':
                label_ROI_control.config(text= 'ROI control- X: ' + str(globals.centreROI['control'][0]) + ' Y: ' + str(globals.centreROI['control'][1]))

    win.bind('p', showROICcontrol)

    def showROICexperimental(event):
        if globals.frames['zabering'][1] == 'on':
                label_ROI_experimental.config(text= 'ROI experimental- X: ' + str(globals.centreROI['experimental'][0]) + ' Y: ' + str(globals.centreROI['experimental'][1]))

    win.bind('i', showROICexperimental)


    ########################################################################################
    ### TACTILE HEIGHT
    ########################################################################################

    globals.pressure = StringVar(globals.frames['tactile_height'][0])
    globals.pressure.set('Start')

    label_tactile_height = Label(globals.frames['tactile_height'][0], textvariable=globals.pressure,
        bg = 'black', fg = 'white', font = "none 30 bold", anchor = CENTER)

    label_tactile_height.place(x=center[0], y=center[1], anchor="center")


    tactile_height = Frame(globals.frames['tactile_height'][0], width=100, height=100)
    tactile_height.grid(row=0, column=0, sticky='news')
    tactile_height.configure(background = 'black')
    # big_three.place(x=width*0, y=height*0)

    instructions_double =    "Controls:\n  - letter 't' for EXPERIMENTAL\n - letter 'n' for CONTROL\n\n  - letter 'c' to close shutter\n  - letter 'o' to open shutter\n\n  - letter 'h' to home all zabers\n  - press 'enter' to terminate\n\n  - press arrow 'up' to move x axis forward\n  - press arrow 'down' to move x axis backwards\n  - press arrow 'left' to move y axis forward\n  - press arrow 'right' to move y axis backwards\n  - letter 'd' to move Z axis down\n  - letter 'u' to move Z axis up\n\n  - letter 'q' to save CONTROL spot position\n  - letter 'w' to save EXPERIMENTAL spot position\n"

    label_instructions_double = Label(tactile_height, text=instructions_double,
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_instructions_double.pack() #

    label_position_tactile_experimental_pressure = Label(tactile_height, text="Tactile experimental- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_tactile_experimental_pressure.pack() #place(x=width*0.10, y=height*0.18)

    label_position_tactile_control_pressure = Label(tactile_height, text="Tactile control- X:     Y:     Z: ",
        bg = 'black', fg = 'white', font="none 12", justify=LEFT)

    label_position_tactile_control_pressure.pack() #place(x=width*0.10, y=height*0.20)

    def showPosExpTact(event):
        if globals.frames['tactile_height'][1] == 'on':

            if globals.current_device == 'tactile':
                label_position_tactile_experimental_pressure.config(text= 'Tactile experimental-X: ' + str(globals.positions['tactile']['experimental'][0]) + ' Y: ' + str(globals.positions['tactile']['experimental'][1]) + ' Z: ' + str(globals.positions['tactile']['experimental'][2]))

    win.bind('w', showPosExpTact)

    def showPosConTact(event):
        if globals.frames['tactile_height'][1] == 'on':

            if globals.current_device == 'tactile':
                label_position_tactile_control_pressure.config(text= 'Tactile control-X: ' + str(globals.positions['tactile']['control'][0]) + ' Y: ' + str(globals.positions['tactile']['control'][1]) + ' Z: ' + str(globals.positions['tactile']['control'][2]))


    win.bind('q', showPosConTact)

    ########################################################################################
    ### INTRO TACTILE HEIGHT
    ########################################################################################

    label_intro_tactile_height = Label(globals.frames['intro_tactile_height'][0], text="Now, we are going to find the pressure that the tactile stimulator exerts on your skin",
        bg = 'black', fg = 'white', font = "none 30 bold", anchor = CENTER)

    label_intro_tactile_height.place(x=center[0], y=center[1], anchor="center")


    ########################################################################################
    #################################  BIG THREE INTRO
    ########################################################################################
    label_intro_big_three = Label(globals.frames['intro_big_three'][0], text="Now, we are going to find the positions for the robots",
        bg = 'black', fg = 'white', font = "none 30 bold", anchor = CENTER)

    label_intro_big_three.place(x=center[0], y=center[1], anchor="center")

    ########################################################################################
    #################################  TRAINING INTRO
    ########################################################################################
    label_intro_training = Label(globals.frames['intro_training'][0], text="We are about to start the experiment, let's practice first",
        bg = 'black', fg = 'white', font = "none 30 bold", anchor = CENTER)

    label_intro_training.place(x=center[0], y=center[1], anchor="center")

    ########################################################################################
    #################################  TRAINING REPEAT
    ########################################################################################
    def testValRepeatTrain(ans, acttyp):

        if acttyp == '1': #insert
            if ans != 'y' and ans != 'n':
                print(ans)
                return False
        return True


    label_repeat_training1 = Label(globals.frames['repeat_training'][0], text="Are we ready to start? (y/n)", bg = 'black', fg = 'white',
        font = "none 30 bold", anchor = CENTER)

    label_repeat_training2 = Label(globals.frames['repeat_training'][0], text="{}".format('\n\n Type your answer \n and press ENTER'), bg = 'black', fg = 'white',
        font = "none 15 bold", anchor = CENTER)

    entry_repeat_training = Entry(globals.frames['repeat_training'][0], validate = "key")
    entry_repeat_training['validatecommand'] = (entry_repeat_training.register(testValRepeatTrain),'%P','%d')

    label_repeat_training1.place(x=center[0], y=center[1], anchor="center")
    label_repeat_training2.place(x=center[0] + 350, y=center[1] + 40, anchor="center")
    entry_response.place(x=center[0]+ 300, y=center[1], anchor="center")

    ########################################################################################
    #################################  TRIALS INTRO
    ########################################################################################
    label_intro_trials = Label(globals.frames['intro_trials'][0], text="Now, we are going to start the experiment. Press enter to begin!",
        bg = 'black', fg = 'white', font = "none 30 bold", anchor = CENTER)

    label_intro_trials.place(x=center[0], y=center[1], anchor="center")



    ########################################################################################
    ########################################################################################
    ############ Start experiment
    ########################################################################################
    ########################################################################################

    eng = me.start_matlab()
    thread_experiment = threading.Thread(target = experiment, args=[eng], daemon = True)
    thread_experiment.start()

    raise_frame(globals.frames['start'][0])
    ani_zabering = animation.FuncAnimation(fig_zabering, animate_zabering, interval=10, blit=False)

    win.mainloop()

############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################

    # # Bind event to show TACTILE positions
    # def showTactilePosExp(event):
    #     if globals.frames['zabering'][1] == 'on':
    #         print('we are at the tactile')
    #         label_position_tactile_experimental.config(text= 'Tactile experimental-X: ' + str(globals.positions['tactile']['experimental'][0]) + ' Y: ' + str(globals.positions['tactile']['experimental'][1]) + ' Z: ' + str(globals.positions['tactile']['experimental'][2]))
    #
    # win.bind('x', showTactilePosExp)
    #
    # def showTactilePosCon(event):
    #     if globals.frames['zabering'][1] == 'on':
    #         print('we are at the tactile')
    #         label_position_tactile_control.config(text= 'Tactile control-X: ' + str(globals.positions['tactile']['control'][0]) + ' Y: ' + str(globals.positions['tactile']['control'][1]) + ' Z: ' + str(globals.positions['colther']['control'][2]))
    # win.bind('z', showTactilePosCon)
    #
    # # Bind event to show CAMERA positions
    # def showCameraPosExp(event):
    #     if globals.frames['zabering'][1] == 'on':
    #         label_position_zabering_experimental.config(text= 'Camera experimental-X: ' + str(globals.positions['camera']['experimental'][0]) + ' Y: ' + str(globals.positions['camera']['experimental'][1]) + ' Z: ' + str(globals.positions['camera']['experimental'][2]))
    # win.bind('x', showCameraPosExp)
    #
    # def showCameraPosCon(event):
    #     if globals.frames['zabering'][1] == 'on':
    #         print('we are at the camera')
    #         label_position_zabering_control.config(text= 'Camera control-X: ' + str(globals.positions['camera']['control'][0]) + ' Y: ' + str(globals.positions['camera']['control'][1]) + ' Z: ' + str(globals.positions['camera']['control'][2]))
    # win.bind('z', showCameraPosCon)


    # ########################################################################################
    # ### RESPONSE SENSITIVITY
    # ########################################################################################
    # def testValSensi(ans, acttyp):
    #
    #     if acttyp == '1': #insert
    #         if ans != 'y' & ans != 'n':
    #             return False
    #
    #     return True
    #
    #
    # label_sensi1 = Label(globals.frames['response_sensi'][0], text="Did you feel anything?", bg = 'black', fg = 'white',
    #     font = "none 30 bold", anchor = CENTER)
    #
    # label_sensi2 = Label(globals.frames['response_sensi'][0], text="{}".format('\n\n Type your answer \n and press ENTER'), bg = 'black', fg = 'white',
    #     font = "none 15 bold", anchor = CENTER)
    #
    # entry_sensi = Entry(globals.frames['response_sensi'][0], validate = "key")
    # entry_sensi['validatecommand'] = (entry_sensi.register(testValSensi),'%P','%d')
    #
    # label_sensi1.place(x=center[0] - 100, y=center[1], anchor="center")
    # label_sensi2.place(x=center[0], y=center[1], anchor="center")
    # entry_sensi.place(x=center[0]+ 40, y=center[1] + 40, anchor="center")
    #
    # ########################################################################################
    # ### RESPONSE DISCRIMINATION
    # ########################################################################################
    #
    # def testValSensi(ans, acttyp):
    #
    #     if acttyp == '1': #insert
    #         if ans != 'y' & ans != 'n':
    #             return False
    #
    #     return True
    #
    #
    # label_discri1 = Label(globals.frames['response_discri'][0], text="Did it feel cold? (y/n)", bg = 'black', fg = 'white',
    #     font = "none 30 bold", anchor = CENTER)
    #
    # label_discri2 = Label(globals.frames['response_discri'][0], text="{}".format('\n\n Click on the box, type your answer \n and press enter'), bg = 'black', fg = 'white',
    #     font = "none 15 bold", anchor = CENTER)
    #
    #
    # entry_discri = Entry(globals.frames['response_discri'][0], validate = "key")
    # entry_discri['validatecommand'] = (entry_discri.register(testValSensi),'%P','%d')
    #
    # label_discri1.place(x=center[0] - 100, y=center[1], anchor="center")
    # label_discri2.place(x=center[0], y=center[1], anchor="center")
    # entry_discri.place(x=center[0]+ 40, y=center[1] + 40, anchor="center")
    #
    # ########################################################################################
    # #################################  BIG THREE
    # ########################################################################################
    #


    #
    # # Label COLTHER positions
    # label_position_colther_experimental = Label(globals.frames['big_three'][0], text="Colther experimental- X:     Y:     Z: ",
    #     bg = 'black', fg = 'white', font="none 8", anchor = CENTER)
    #
    # label_position_colther_experimental.place(x=width*0.10, y=height*0.13)
    #
    # label_position_colther_control = Label(globals.frames['big_three'][0], text="Colther control- X:     Y:     Z: ",
    #     bg = 'black', fg = 'white', font="none 8", anchor = CENTER)
    #
    # label_position_colther_control.place(x=width*0.10, y=height*0.15)
    #
    #
    # # Label TACTILE positions
    # label_position_tactile_experimental = Label(globals.frames['big_three'][0], text="Tactile experimental- X:     Y:     Z: ",
    #     bg = 'black', fg = 'white', font="none 8", anchor = CENTER)
    #
    # label_position_tactile_experimental.place(x=width*0.10, y=height*0.18)
    #
    # label_position_tactile_control = Label(globals.frames['big_three'][0], text="Tactile control- X:     Y:     Z: ",
    #     bg = 'black', fg = 'white', font="none 8", anchor = CENTER)
    #
    # label_position_tactile_control.place(x=width*0.10, y=height*0.20)
    #
    # # Label CAMERA positions
    # label_position_zabering_experimental = Label(globals.frames['big_three'][0], text="Camera experimental- X:     Y:     Z: ",
    #     bg = 'black', fg = 'white', font="none 8", anchor = CENTER)
    #
    # label_position_zabering_experimental.place(x=width*0.10, y=height*0.23)
    #
    # label_position_zabering_control = Label(globals.frames['big_three'][0], text="Camera control- X:     Y:     Z: ",
    #     bg = 'black', fg = 'white', font="none 8", anchor = CENTER)
    #
    # label_position_zabering_control.place(x=width*0.10, y=height*0.25)
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
