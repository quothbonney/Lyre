#!/usr/bin/python3
# Open source software written by Jack D.V. Carson

import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import time
from tkinter import TclError
import wave

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


# pyaudio class instance
p = pyaudio.PyAudio()
wf = wave.open("samples/violin_c.wav", 'rb')

# stream object to get data from microphone
stream = p.open(
    frames_per_buffer=CHUNK,
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=wf.getframerate(),
    output=True,
)

# variable for plotting
x = np.arange(0, 4 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK*2)     # frequencies (spectrum)

# create a line object with random data

# create semilogx line for spectrum

# format waveform axes

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()


# binary data
data = wf.readframes(CHUNK)  
    
# convert data to integers, make np array, then offset it by 127
data_int = struct.unpack(str(4 * CHUNK) + 'B', data)
    
# create np array and offset by 128
data_np = np.array(data_int, dtype='b')[::2] + 128

# create matplotlib figure and axes

# pyaudio class instance
p = pyaudio.PyAudio()
wf = wave.open("samples/violin_c.wav", 'rb')

# stream object to get data from microphone
stream = p.open(
    frames_per_buffer=CHUNK,
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=wf.getframerate(),
    output=True,
)

# variable for plotting
x = np.arange(0, 4 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK*2)     # frequencies (spectrum)

# format waveform axes
plt.title('AUDIO WAVEFORM')
plt.xlabel('samples')
plt.ylabel('volume')

# format spectrum axes

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()


# binary data
data = wf.readframes(CHUNK)  
    
# convert data to integers, make np array, then offset it by 127
data_int = struct.unpack(str(4 * CHUNK) + 'B', data)
    
# create np array and offset by 128
data_np = np.array(data_int, dtype='b')[::2] + 128

yf = fft(data_int)

plt.plot(np.abs(yf))
plt.show()
