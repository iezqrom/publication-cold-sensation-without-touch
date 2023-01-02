################################ Import stuff ################################
# %%
from classes_arduino import ArdUIno
from classes_arduino import *
from classes_colther import Zaber
from classes_colther import *
from classes_camera import TherCam
from saving_data import *
from classes_text import TextIO
from grabPorts import grabPorts
from classes_audio import Sound
from classes_conds import ConditionsHandler
from classes_conds import *
from classes_testData import TestingDataHandler
from failing import *
from saving_data import *
from classes_speech import *
from classes_audio import Sound

import subprocess
import os
import globals
import time
import threading
import random
import numpy as np
import simpleaudio as sa
import keyboard
import math
from datetime import date
import pyttsx3
import psutil
from rand_cons import *
import argparse
import wave

from index_funcs import *

from saving_data import *

from classes_tharnalBeta import ReAnRaw
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3

colorMapType = 0
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation

### Data structure
import numpy as np

## Media
from imutils.video import VideoStream
from classes_tharnal import *
from classes_plotting import *
from datetime import date
from saving_data import *


# %%
# mol_videos_name = f'mol_subj2_'

# pattern = f'{mol_videos_name}.*\.hdf5$'

# patternc = re.compile(pattern)
# names = []

# for filename in os.listdir(f'../../src_analysis/test_04122020/videos'):
#     # print(filename)
#     if patternc.match(filename):
#         name, form = filename.split('.')
#         names.append(name)
#         print(name)
#     else:
#         continue


# path_day, path_anal, path_figs, path_data, path_videos, path_audios = mkpaths('tb')
# t1 = ReAnRaw(f'{path_videos}/mol_subj3_trial4_pos9')
# t1.datatoDic()
# print(t1.data['diff_coor'])
# t1.extractMeansF(name_coorF = 'diff_coor')
# last_temp.append(t1.means[-1])



# %%
if __name__ == "__main__":

    speaker = initSpeak()
    speech_to_text = initSpeech2Text()
    beep_speech_success = Sound(1000, 0.2)
    beep = Sound(400, 6)

    beep.play()
    time.sleep(7)

    audio = startAudioWatson()
    audio_source, q = audioInstance()
    stream = openStream(audio, q)
    recognize_yes_no = Thread(target=recognize_yes_no_weboscket, args=[speech_to_text, audio_source, globals.answer])
    recognize_yes_no.name = 'Speech recognition thread'
    recognize_yes_no.start()

    stream.start_stream()

    qs = 'Was there any temperature change during the tone?' # el pavo dice: Was there any temperature change during the tone?
    speak(speaker, qs)
    start = time.time()

    globals.answer = None
    globals.answered = None

    

    beep_speech_success.play()

    end = time.time() - start
    print(end)

    while True:
        if globals.answer == 1:
            if globals.answered == 1 or globals.answered == 0:
                print('Answered', globals.answered)
                break
            
    terminateSpeechRecognition(stream, audio, audio_source)

    beep_speech_success.play()



# %%    
    # dat_im = ReAnRaw(f'../../src_analysis/test_04122020/videos/mol_subj2_trial4_pos3')
    # dat_im.datatoDic()
    # dat_im.extractMeansF()

    # Writer = animation.writers['ffmpeg']
    # writer = Writer(fps = 9, metadata=dict(artist='Me'), bitrate=1800)
    # vminT = -1
    # vmaxT = 3
    # diff_buffer = []
    # # print(dat_im.data['stimulus'])

    # def animate(i, data, plots, axs, fixed_coor, dynamic_coor, eu, means, diff_buffer, shutter_pos):
    #     widthtick = 3
    #     title_pad = 20
    #     lwD = 5
    #     widthtick = 5
    #     lenD = 15

    #     r = 20

    #     # First subplot: 2D RAW
    #     ax1.clear()
    #     # print(eu[i])

    #     circles = []
    #     # if eu[i] < 20:
    #     #     roi = dynamic_coor[i][:, 0][::-1]
    #     # else:
    #     #     roi = fixed_coor[i][::-1]
            
    #     # cirD = plt.Circle(dynamic_coor[i][:, 0][::-1], r, color='r', fill = False, lw=lwD*1.2)
    #     x = np.arange(0,160,1)
    #     y = np.arange(0,120,1)

    #     xs, ys = np.meshgrid(x, y)
    #     zs = (xs*0 + 15) + (ys*0 + 15)

    #     if i > 15 and i < 18:
    #         print('saving diff buff')
    #         diff_buffer.append(data[i])

    #     print(shutter_pos[i])

    #     if i > 22:
    #         mean_diff_buffer = np.mean(diff_buffer, axis=0)
    #         dif = mean_diff_buffer - data[i]
    #         maxdif = np.max(dif)
    #         indydf, indxdf = np.where(dif == maxdif)
    #         roi = [indxdf[0], indydf[0]]
    #         image = dif
    #         print('performing diff')
    #     else:
    #         image = data[i]
    #         roi = fixed_coor[i][::-1]

    #     ax1.imshow(image, cmap='hot', vmin = vminT, vmax = vmaxT)
    
    #     cir = plt.Circle(roi, r, color='b', fill = False, lw=lwD*1.2)
    #     # print([indyDf, indxDf])
    #     ax1.add_artist(cir)
    #     # ax1.add_artist(cirD)

    #     ax1.set_title('Thermal image', pad = title_pad)
    #     ax1.set_axis_off()

    #     # # Second subplot: Euclidean distance
    #     ax2.clear()
    #     ax2.plot(eu[0:i + 1], lw= lwD*1.2, color = 'black')
    #     ax2.set_ylim(0, 100)
    #     ax2.set_xlim([0, len(eu)])

    #     ax2.set_title('Euclidean distance', pad = title_pad)

    #     steps = 2
    #     # framesToseconds(ax2, 2, eu)

    #     ax2.spines['top'].set_visible(False)
    #     ax2.spines['right'].set_visible(False)

    #     ax2.yaxis.set_tick_params(width = lwD, length = lenD)
    #     ax2.xaxis.set_tick_params(width = lwD, length = lenD)

    #     ax2.tick_params(axis='y', which='major', pad=10)
    #     ax2.tick_params(axis='x', which='major', pad=10)

    #     ax2.spines['left'].set_linewidth(lwD)
    #     ax2.spines['bottom'].set_linewidth(lwD)
    #     ax2.set_xlabel('Time (s)')

    #     # MEAN TEMPERATURE
    #     r = 20
    #     xs = np.arange(0, 160)
    #     ys = np.arange(0, 120)

    #     ax3.clear()
    #     ax3.plot(means[0:i + 1], lw= lwD*1.2, color = '#007CB7')
    #     ax3.set_ylim([27, 34])
    #     ax3.set_xlim([0, len(means)])
    #     ax3.set_title('Mean temperature fixed ROI', pad = title_pad)

    #     steps = 2
    #     framesToseconds(ax3, 2, eu)

    #     ax3.spines['top'].set_visible(False)
    #     ax3.spines['right'].set_visible(False)

    #     ax3.yaxis.set_tick_params(width = lwD, length = lenD)
    #     ax3.xaxis.set_tick_params(width = lwD, length = lenD)

    #     ax3.tick_params(axis='y', which='major', pad=10)
    #     ax3.tick_params(axis='x', which='major', pad=10)

    #     ax3.spines['left'].set_linewidth(lwD)
    #     ax3.spines['bottom'].set_linewidth(lwD)
    #     ax3.set_xlabel('Time (s)')
    #     plt.tight_layout()

    # ################ Plot figure
    # fig = plt.figure(figsize = (35, 10))

    # mc = 'black'
    # plt.rcParams.update({'font.size': 40, 
    #                         'axes.labelcolor' : "{}".format(mc), 
    #                         'xtick.color': "{}".format(mc),
    #                         'ytick.color': "{}".format(mc),
    #                         'font.family': 'sans-serif'})

    # #######################Axes
    # ax1 = fig.add_subplot(131)
    # ax2 = fig.add_subplot(132)
    # ax3 = fig.add_subplot(133)

    # x = np.arange(0,160,1)
    # y = np.arange(0,120,1)

    # xs, ys = np.meshgrid(x, y)
    # zs = (xs*0 + 15) + (ys*0 + 15)

    # ######################Plots
    # ## First subplot: 2D video
    # plot1 = ax1.imshow(zs, cmap='hot', vmin = vminT, vmax = vmaxT)
    # cb = fig.colorbar(plot1, ax = ax1)
    # cb.set_ticks(np.arange(vminT, (vmaxT + 0.01), 1))

    # ## Second subplot: eu distance
    # plot2 = ax2.plot(np.arange(len(dat_im.data['eu'])), np.arange(len(dat_im.data['eu'])), color =  'black')

    # ## Third subplot: mean ROI
    # plot3 = ax3.plot(np.arange(len(dat_im.data['image'])), np.arange(len(dat_im.data['image'])), color =  'black')

    # #Aesthetics
    # plots = [plot1, plot2, plot3]
    # axes = [ax1, ax2, ax3]
    
    # #Animation & save
    # ani = animation.FuncAnimation(fig, animate, frames = len(dat_im.data['image']), fargs = (dat_im.data['image'], plots, axes, dat_im.data['fixed_coor'], dat_im.data['dynamic_coor'], dat_im.data['eu'], dat_im.means, diff_buffer, dat_im.data['stimulus']), interval=1000/8.7)

    # mp4_name = 'mp4_' + 'sdt_test'
    # ani.save(f'./{mp4_name}.mp4', writer = writer)

    # fig.clf()



# %%

    # speaker = initSpeak()
    # qs = 'Test test'
    # speak(speaker, qs)
    
    # speaker = initSpeak()
    # speech_to_text = initSpeech2Text()
    # beep_speech_success = Sound(1000, 0.2)
    # beep = Sound(400, 40)
    # channels = 1
    # fs = 44100
    # # filename = f'{path_audios}/test1.wav'

    # audio = startAudioWatson()
    # audio_source, q = audioInstance()
    # stream = openStream(audio, q)
    # recognize_yes_no = Thread(target=recognize_yes_no_weboscket, args=[speech_to_text, audio_source, globals.answer])
    # recognize_yes_no.name = 'Speech recognition thread'
    # recognize_yes_no.start()

    # stream.start_stream()

    # qs = 'Was there any temperature change during the tone?' # el pavo dice: Was there any temperature change during the tone?
    # speak(speaker, qs)
    # start = time.time()

    # globals.answer = None
    # globals.answered = None

    # beep_speech_success.play()

    # end = time.time() - start
    # print(end)

    # while True:
    #     print(globals.answer)
    #     if globals.answer == 1:
    #         if globals.answered == 1 or globals.answered == 0:
    #             print('Answered', globals.answered)
    #             break
            
    # terminateSpeechRecognition(stream, audio, audio_source)

    # beep_speech_success.play()

    # print(globals.frames)

    # Save the recorded data as a WAV file
    # write(f'./output.wav', fs, globals.frames)


# %%

# if __name__ == "__main__":

#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 1
#     RATE = 44100
#     RECORD_SECONDS = 5
#     WAVE_OUTPUT_FILENAME = "output.wav"

#     p = pyaudio.PyAudio()

#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

#     print("* recording")

#     frames = []

#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         frames.append(data)

#     print("* done recording")

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     wf.setnchannels(CHANNELS)
#     print(p.get_sample_size(FORMAT))
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()

    # chunk = 1024  # Record in chunks of 1024 samples
    # sample_format = pyaudio.paInt16  # 16 bits per sample
    # channels = 1
    # fs = 44100  # Record at 44100 samples per second
    # seconds = 3
    # filename = "output.wav"

    # p = pyaudio.PyAudio()  # Create an interface to PortAudio
    # stream.start_stream()

    # print('Recording')

    # frames = []  # Initialize array to store frames

    # for i in range(0, int(fs / chunk * seconds)):
    #     data = stream.read(chunk)
    #     frames.append(data)
    #     print('Loop')

    # # Stop and close the stream 
    # stream.stop_stream()
    # stream.close()
    # # Terminate the PortAudio interface
    # p.terminate()

    # write(f'output.wav', fs, globals.frames)
    # wf = wave.open(filename, 'wb')
    # wf.setnchannels(channels)
    # print(p.get_sample_size(sample_format))
    # wf.setsampwidth(p.get_sample_size(sample_format))
    # wf.setframerate(fs)
    # wf.writeframes(b''.join(frames))
    # wf.close()



# %%
# if __name__ == "__main__":

    # fs = 44100  # Sample rate
    # seconds = 3  # Duration of recording


    # speech_to_text = initSpeech2Text()
    # audio = startAudioWatson()
    # audio_source, q = audioInstance()
    # beep_speech_success = Sound(1000, 0.2)
    # stream = openStream(audio, q)
    # recognize_yes_no = Thread(target=recognize_yes_no_weboscket, args=[speech_to_text, audio_source, globals.answer])
    # recognize_yes_no.name = 'Speech recognition thread'
    # recognize_yes_no.start()

    #     myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    #     stream.start_stream()

    #     print('Started recording')

    #     while True:
    #         if globals.answer == 1:
    #             if globals.answered == 1 or globals.answered == 0:
    #                 print('Answered', globals.answered)
    #                 break

    #     if globals.answered == 1:
    #         yeses.append(globals.answered)
    #     elif globals.answered == 0:
    #         noses.append(globals.answered)

    #     print(f'{len(yeses)} yeses')
    #     print(f'{len(noses)} noses')

    #     terminateSpeechRecognition(stream, audio, audio_source)

    #     sd.wait()  # Wait until recording is finished
    #     write(f'wat_val6_{i}_{globals.answered}.wav', fs, myrecording)  # Save as WAV file 

    #     beep_speech_success.play()

    #     globals.answer = None
    #     globals.answered = None
    #     time.sleep(1)



# if __name__ == "__main__":
#     # path_day, path_anal, path_figs, path_data, path_videos = mkpaths(situ)

#     zabers = set_up_big_three(globals.axes)
#     homingZabersConcu(zabers, globals.haxes)

#     for k, v in globals.haxes.items():
#         if k == 'tactile':
#             printme('Not moving tactile for mol')
#         else:
#             movetostartZabersConcu(zabers, k, list(reversed(v)), pos = globals.positions[k])
#             time.sleep(0.1)

#     homingZabersConcu(zabers, globals.haxes)


# if __name__ == "__main__":

#     try:
#         ports = grabPorts()
#         print(ports.ports)

#         arduino_shutter = ArdUIno(usb_port = 1, n_modem = 1)
#         arduino_shutter.arduino.flushInput()

#         zabers = set_up_big_three(globals.axes)
#         homingZabersConcu(zabers, globals.haxes)

#         cam = TherCam()
#         cam.startStream()
#         cam.setShutterManual()

#         try:
#             globals.positions = csvtoDictZaber(path_data)
#             print(globals.positions)
#         except:
#             printme('No temporary file for Zaber positions')
        

#         # shakeShutter(arduino_shutter, 5)

#         printme('Check Zaber sets are working')

#         park_camera = {'x': 357507, 'y': 410000, 'z': 316955}
#         park_colther = {'x': 269236, 'y': 255070, 'z': 54784}

#         movetostartZabersConcu(zabers, 'camera', globals.haxes['camera'], pos = park_camera)
#         movetostartZabersConcu(zabers, 'colther', globals.haxes['colther'], pos = park_colther)

#         manual = threading.Thread(target = zabers['colther']['x'].manualCon3, args = [zabers, arduino_shutter, 'n'], daemon = True)
#         manual.start()

#         cam.plotLiveROINE()

#         homingZabersConcu(zabers, globals.haxes)

#         # print(globals.positions)

#     except Exception as e:
#         globals.stimulus = 0
#         arduino_shutter.arduino.write(struct.pack('>B', globals.stimulus))

#         # rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
#         # changeNameTempFile(path_data)
        
#         errorloc(e)

#     except KeyboardInterrupt:
#         print('Keyboard Interrupt')
#         globals.stimulus = 0
#         arduino_shutter.arduino.write(struct.pack('>B', globals.stimulus))

        # rootToUser(path_day, path_anal, path_data, path_figs, path_videos)
        # changeNameTempFile(path_data)
        




# todaydate = '27112020'
# folder_name = "test_" + todaydate
# os.chdir('/Users/ivanezqrom/Documents/AAA_online_stuff/Coding/python/phd/expt4_py_nontactileCold/src_analysis')
# print(folder_name)

# # %% SUBJECT
# subj = 1
# pattern = f'mol_{subj}.*\.hdf5$'
# # pattern = f'mol_subj{subj}.*\.hdf5$'
    
# patternc = re.compile(pattern)
# names = []

# for filename in os.listdir(f'./{folder_name}/videos/'):
#     if patternc.match(filename):
#         print(filename)
#         name, form = filename.split('.')
#         names.append(name)
#     else:
#         continue

# names.sort(key=natural_keys)
# print(names)

# # %%
# dat_im = ReAnRaw(f'./{folder_name}/videos/{names[0]}')
# dat_im.datatoDic()
# dat_im.extractMeansF()

# %%
# p = tactile3.device.send("/home")
# p.data


# %%
# tactile1.home()

# %%

# # %%
# n_trials = 9
# conditions = 2    
# stims = sdt_setup(n_trials, conditions)

# init_pos = np.arange(1, 9.01, 1)
# init_rep = np.repeat(init_pos, 1)
# np.random.shuffle(init_rep)
# final_order = exp_rand(init_rep, check_twoD, coor_cells=globals.coor_cells)

# # %%

# for i, s in enumerate(stims):
#     p = str(final_order[i])
#     print(p)


# # %%
# n_trials = 13
# conds = 2

# stimulations = []

# if not n_trials % (2*conds) == 0:
#     printme(f'Number of trials is not divisable by {2*conds}')
#     if not n_trials % 2 == 0:
#         printme(f'Number of trials is an odd number')
#     printme('WARNING: Uneven number of conditions')
#     code_conds = np.arange(conds)
#     n_cond_trials = n_trials/conds

#     n_conds = np.repeat(code_conds, n_cond_trials, axis = 0)
#     unique, counts = np.unique(n_conds, return_counts=True)
#     print(counts)
    
#     for u, c in zip(unique, counts):
#         abs_pres = np.repeat([0, 1], c, axis = 0)
        
#         for ap in abs_pres:
#             stimulations.append((u, ap))

#     np.random.shuffle(stimulations)
#     stimulations = stimulations[:n_trials]
    
# else:
#     code_conds = np.arange(conds)
#     n_cond_trials = n_trials/conds

#     n_conds = np.repeat(code_conds, n_cond_trials, axis = 0)
#     unique, counts = np.unique(n_conds, return_counts=True)
#     # print(counts)
    
#     for u, c in zip(unique, counts):
#         print(c/2)
#         abs_pres = np.repeat([0, 1], c/2, axis = 0)
        
#         for ap in abs_pres:
#             stimulations.append((u, ap))

#     np.random.shuffle(stimulations)



# # %%
# conds = 2
# n_trials = 9

# code_conds = np.arange(conds)

# n_conds = np.repeat(code_conds, n_trials, axis = 0)
# # print(n_conds)
# unique, counts = np.unique(n_conds, return_counts=True)
# # print(counts)

# stimulations = []
# for u, c in zip(unique, counts):
#     abs_pres = np.repeat([0, 1], c/2, axis = 0)
#     # print(abs_pres)
    
#     for ap in abs_pres:
#         # print(ap)
#         stimulations.append((u, ap))

# np.random.shuffle(stimulations)
# print(len(stimulations))

# %%
# a = 1
# l = [1, 4, 7]

# if any(v == a for v in l):
#     print('column 1')

# %%

# z_axis_pos(4, 0.1905)

# n_trials = 36
# conditions = 2    
# stims = sdt_setup(n_trials, conditions)

# init_pos = np.arange(1, 9.01, 1)
# init_rep = np.repeat(init_pos, 4)
# np.random.shuffle(init_rep)
# final_order = exp_rand(init_rep, check_twoD, coor_cells=globals.coor_cells)
# %%
# globals.grid = csvToDictGridAll(path_data)

# a = globals.grid['camera']['1'].copy()

# a['z'] = 0


# # %%

# path_day, path_anal, path_figs, path_data = folderChreation()
# path_videos = folderVhrideos()
# # Recover data
# globals.positions = csvtoDictZaber(path_data)
# # globals.haxes = manualorder(globals.haxes)
# saveHaxesAll(path_data, globals.haxes)

# print(f"\nPositions Zabers: {globals.positions}\n")
# print(f"\nHaxes: {globals.haxes}")

# zabers = set_up_big_three(globals.axes)
# homingZabersConcu(zabers)

# arduino_shutter = ArdUIno(usb_port = 1, n_modem = 1)
# arduino_shutter.arduino.flushInput()

# cam = TherCam()
# cam.startStream()

# for k, v in reversed(globals.haxes.items()):
#     # if k != 'tactile':
#         movetostartZabersConcu(zabers, k, v, pos = globals.positions[k])

# cam.setShutterManual()

# manual = threading.Thread(target = zabers['colther']['x'].manualCon3, args = [zabers, arduino_shutter, 'n'], daemon = True)
# manual.start()

# cam.plotLiveROINE()

# homingZabers(zabers, globals.haxes)

# situ = 'tb'
# if situ == 'ex':
#     n_trials = 144
#     conditions = 2    
#     stims = sdt_setup(n_trials, conditions)

#     init_pos = np.arange(1, 9.01, 1)
#     init_rep = np.repeat(init_pos, 16)
#     np.random.shuffle(init_rep)
#     final_order = exp_rand(init_rep, check_twoD, globals.coor_cells)

# elif situ == 'tb':
#     n_trials = 36
#     conditions = 2    
#     stims = sdt_setup(n_trials, conditions)

#     init_pos = np.arange(1, 9.01, 1)
#     init_rep = np.repeat(init_pos, 16)
#     np.random.shuffle(init_rep)
#     final_order = exp_rand(init_rep, check_twoD, coor_cells= globals.coor_cells, restart=600)

# print(final_order)


# if __name__ == "__main__":
#     arduino_shutter = ArdUIno(usb_port = 1, n_modem = 1)
#     arduino_shutter.arduino.flushInput()

#     time.sleep(1)

#     while True:
#         a = input('input:  ')
#         arduino_shutter.arduino.write(struct.pack('>B', int(a)))



# %%


# a = [3, 5, 1, 7, 9, 5, 3, 9, 7, 1, 6, 8, 2, 6, 8]

# unique_elements, counts_elements = np.unique(a, return_counts=True)
# print(unique_elements, counts_elements)
# time.sleep(0.1)

# ar = prob_choice(counts_elements)

# # %%

# t = []
# for i in np.arange(100000):
#     c = np.random.choice(unique_elements, 1, replace=True, p=ar)
#     t.append(c)

# print('end')
# # %%
# tt = np.asarray(t)

# np.unique(tt, return_counts=True)

# # %%


# ditc1 = {"P01":{"x":0.4,"x":0.6}, "P02":{"F2":0.3, "P03":0.7}, "P03":{"F3":0.2, "P02":0.8}}

# expressions = []
# for p, equation_components in ditc1.items():
#     p = Symbol(p)
#     print(p)
#     expression = []
#     for name, multiplier in equation_components.items():
#         expression.append(Symbol(name) * multiplier)
#     expressions.append(Eq(1, Add(*expression)))

# # %%

# x = symbols('x')
# print(x)
# #%%

# raw_p = [1, 1, 0.5]
# exprs = []
# for i in raw_p:
#     exprs.append(Symbol('x') * i/3)

# ex = Eq(1, Add(*exprs))
# print(ex)

# sol = solve(ex)

# sol

# # %%
# [(v*sol[0])/3 for v in raw_p]

# # %%
# ar = [1, 1, 0.5]
# prob = [x * a for a in ar]


# %%

# print('python on')
# parser = argparse.ArgumentParser(description='Test')

# parser.add_argument("-s", type=str)
# args = parser.parse_args()

# situ = args.s
# print(situ)

# if situ == 'ex':
#     trials_per_cell = 10
#     cells = [1, 2, 3, 4]
#     init_rep = np.repeat(cells, trials_per_cell)
#     np.random.shuffle(init_rep)

#     final_order = exp_rand(init_rep, check_linear)

# elif situ == 'tb':
#     trials_per_cell = 1
#     cells = [1, 2, 3, 4]
#     init_rep = np.repeat(cells, trials_per_cell)
#     np.random.shuffle(init_rep)

#     final_order = exp_rand(init_rep, check_linear)

# print(final_order)



# %%
# print('python on')
# parser = argparse.ArgumentParser(description='Test')

# parser.add_argument("-t", type=str)
# args = parser.parse_args()

# t = args.t
# print(t)


# if __name__ == "__main__":
#     zabers = set_up_big_three(globals.axes)
#     homingZabersConcu(zabers, globals.haxes)

#     # arduino_shutter = ArdUIno(usb_port = 1, n_modem = 1)
#     # arduino_shutter.arduino.flushInput()

#     # zabers['colther']['x'].manualCon3(zabers, arduino_shutter, 'n')
#     pos_init = {'x': 300000, 'y': 90000, 'z': 0}
#     pos_knuckle = {'x': 250000, 'y': 180000, 'z': 0}
#     centre_y = z_axis_pos(3, globals.step_sizes['colther'])

#     pos_centre = {'x': 250000, 'y': (180000 + centre_y), 'z': 0}
 
#     while True:
#         if keyboard.is_pressed('i'):
#             movetostartZabersConcu(zabers, 'colther', list(reversed(globals.haxes['colther'])), pos = pos_init)
        
#         elif keyboard.is_pressed('k'):
#             movetostartZabersConcu(zabers, 'colther', list(reversed(globals.haxes['colther'])), pos = pos_knuckle)

#         elif keyboard.is_pressed('f'):
#             movetostartZabersConcu(zabers, 'colther', list(reversed(globals.haxes['colther'])), pos = pos_centre)

#         elif keyboard.is_pressed('e'):
#             break

#     print('DONE')


# %%

# def rem_chosen(val_left, current_chosen):
#     """
#         Function to remove one occurrence of an integer in a numpy array
#     """
#     where_chosen = np.argwhere(val_left == current_chosen).flatten()
#     remove_one_chosen = np.random.choice(where_chosen)
#     val_left = np.delete(val_left, remove_one_chosen)
#     return val_left

# def check_twoD(ordered_array, current_chosen, i, coords):
#     """
#         Function to check whether a chosen position is valid in a 2-D grid (n x n)
#     """
#     previous_chosen = ordered_array[-int(i)]
#     previous_coords = coords[str(int(previous_chosen))]
#     current_coords = coords[str(int(current_chosen))]
    
#     row_diff = abs(current_coords[0] - previous_coords[0])
#     column_diff = abs(current_coords[1] - previous_coords[1])
    
#     if row_diff != column_diff and any(c == 1 for c in [row_diff, column_diff]) and any(c == 0 for c in [row_diff, column_diff]):
#         print(f'\nInvalid choice at position {-int(i)}\n')
#         return False
#     elif previous_chosen == current_chosen[0]:
#         print(f'\nInvalid choice at position {-int(i)}\n')
#         return False
#     else:
#         print(f'\nValid choice at position {-int(i)}\n')
#         return True


# def check_linear(ordered_array, current_chosen, i, coords = None):
#     """
#         Function to check whether a chosen position is valid in a line
#     """
#     previous_chosen = ordered_array[-int(i)]
    
#     if previous_chosen == current_chosen[0]:
#         print(f'\nInvalid choice at position {-int(i)}\n')
#         return False
#     else:
#         print(f'\nValid choice at position {-int(i)}\n')
#         return True

# def randomise_constraints(val_left, ordered_array, count, func, limit = 2, coords= None):
#     """
#        Recursive function to randomise with constraints
#     """
#     count += 1
#     if len(val_left) == 0:
#         printme('Constraint randomisation done..')
    
#     elif count > 100:
#         return False

#     elif len(ordered_array) == 0:
#         printme('First value in...')
#         current_chosen = np.random.choice(val_left, 1, replace=False)
#         ordered_array.append(int(current_chosen))
#         val_left = rem_chosen(val_left, current_chosen)
#         randomise_constraints(val_left, ordered_array, count, func, limit, coords)
    
#     else:
#         current_chosen = np.random.choice(val_left, 1, replace=False)
#         backwards = []
#         for i in np.arange(1, limit + 0.1, 1):
#             if len(ordered_array) < i:
#                 break
            
#             current_check = func(ordered_array, current_chosen, i, coords)
#             backwards.append(current_check)

#         if np.all(backwards):
#             print('Another value in...')
#             ordered_array.append(int(current_chosen))
#             val_left = rem_chosen(val_left, current_chosen)
#             randomise_constraints(val_left, ordered_array, count, func, limit, coords)
#         else:
#             randomise_constraints(val_left, ordered_array, count, func, limit, coords)

#     return ordered_array

# def exp_rand(init_rep, check_twoD, coor_cells=None):
#     """
#         Function to converge randomisation with constraints algorithm 
#     """
#     while True:
#         final_order = []
#         final_order = randomise_constraints(init_rep, final_order, 0, check_twoD, coords= coor_cells)
#         if len(final_order) < len(init_rep):
#             printme("Didn't converge...")
#         else:
#             printme('Constraint randomisation done')
#             break
#     return final_order
