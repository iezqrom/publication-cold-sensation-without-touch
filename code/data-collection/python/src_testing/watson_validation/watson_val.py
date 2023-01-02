# %%
from classes_speech import *
from classes_audio import Sound
import globals
import time
import wave
import pyaudio

###############################################
###############################################
###############################################

# %%

import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

yeses = []
noses = []

for i in np.arange(100):

    speech_to_text = initSpeech2Text()
    audio = startAudioWatson()
    audio_source, q = audioInstance()
    beep_speech_success = Sound(1000, 0.2)
    stream = openStream(audio, q)
    recognize_yes_no = Thread(
        target=recognize_yes_no_weboscket,
        args=[speech_to_text, audio_source, globals.answer],
    )
    recognize_yes_no.name = "Speech recognition thread"
    recognize_yes_no.start()

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    stream.start_stream()

    print("Started recording")

    while True:
        if globals.answer == 1:
            if globals.answered == 1 or globals.answered == 0:
                print("Answered", globals.answered)
                break

    if globals.answered == 1:
        yeses.append(globals.answered)
    elif globals.answered == 0:
        noses.append(globals.answered)

    print(f"{len(yeses)} yeses")
    print(f"{len(noses)} noses")

    terminateSpeechRecognition(stream, audio, audio_source)

    sd.wait()  # Wait until recording is finished
    write(f"wat_val6_{i}_{globals.answered}.wav", fs, myrecording)  # Save as WAV file

    beep_speech_success.play()

    globals.answer = None
    globals.answered = None
    time.sleep(1)

# # %%
# import sounddevice as sd
# import soundfile as sf
# from scipy.io import wavfile

# samplingFrequency, signalData = wavfile.read('./test1.wav')
# # Extract data and sampling rate from file
# # data, fs = sf.read(filename, dtype='float32')

# start = int(1.5*44100)
# end = int(3.5*44100)
# sd.play(signalData[start:end], fs)
# status = sd.wait()

# # %%
# audio = startAudioWatson()
# audio_source, q = audioInstance()

# time.sleep(2)

# print(audio.__dict__)
# print(audio_source.__dict__)


# audio.terminate()
# audio_source.completed_recording()

# print(audio.__dict__)
# print(audio_source.__dict__)
# # %%
# speech_to_text = initSpeech2Text()
# audio = startAudioWatson()
# audio_source, q = audioInstance()

# beep_speech_success = Sound(1000, 0.2)
# stream = openStream(audio, q)
# recognize_yes_no = Thread(target=recognize_yes_no_weboscket, args=[speech_to_text, audio_source, globals.answer])
# recognize_yes_no.name = 'Speech recognition thread'
# recognize_yes_no.start()

# chunk = 2048  # Record in chunks of 1024 samples
# sample_format = pyaudio.paInt16  # 16 bits per sample
# channels = 1
# fs = 44100  # Record at 44100 samples per second
# seconds = 2
# filename = "output1.wav"

# p = pyaudio.PyAudio()  # Create an interface to PortAudio

# print('Recording')

# frames = []  # Initialize array to store frames

# # Store data in chunks for 3 seconds
# for i in range(0, int(fs / chunk * seconds)):
#     data = stream.read(chunk, exception_on_overflow=False)
#     frames.append(data)

# print(frames)

# # Stop and close the stream
# stream.stop_stream()
# stream.close()
# # Terminate the PortAudio interface
# p.terminate()

# print('Finished recording')

# # Save the recorded data as a WAV file
# wf = wave.open(filename, 'wb')
# wf.setnchannels(channels)
# wf.setsampwidth(p.get_sample_size(sample_format))
# wf.setframerate(fs)
# wf.writeframes(b''.join(frames))
# wf.close()

# %%
# print(frames[1][40:60])
# # print(map(ord, frames[1][:20]))
# # %%
# filename = 'output.wav'

# # Set chunk size of 1024 samples per data frame
# chunk = 1024

# # Open the sound file
# wf = wave.open(filename, 'rb')

# # Create an interface to PortAudio
# p = pyaudio.PyAudio()

# # Open a .Stream object to write the WAV file to
# # 'output = True' indicates that the sound will be played rather than recorded
# stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
#                 channels = wf.getnchannels(),
#                 rate = wf.getframerate(),
#                 output = True, input_device_index = 0)

# # Read data in chunks
# data = wf.readframes(chunk)

# # Play the sound by writing the audio data to the stream
# while data != '':
#     print(data)
#     stream.write(data)
#     data = wf.readframes(chunk)

# # Close and terminate the stream
# stream.close()
# p.terminate()
# # %%

# import sounddevice as sd
# from scipy.io.wavfile import write

# fs = 44100  # Sample rate
# seconds = 5  # Duration of recording

# myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
# sd.wait()  # Wait until recording is finished
# write('miau7.wav', fs, myrecording)  # Save as WAV file

# # %%
# import sounddevice as sd
# import soundfile as sf
# from scipy.io import wavfile

# filename = './miau7.wav'
# samplingFrequency, signalData = wavfile.read('./output.wav')
# # Extract data and sampling rate from file
# # data, fs = sf.read(filename, dtype='float32')

# start = int(1.5*44100)
# end = int(3.5*44100)
# sd.play(signalData[start:end], fs)
# status = sd.wait()

# %%
