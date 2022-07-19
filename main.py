#!/usr/bin/python3
# Open source software written by Jack D.V. Carson 

import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import numpy as np
import wave
from scipy.io import wavfile
from scipy.signal import find_peaks
from src.notesdict import get_dict
import sys


violin_wav = sys.argv[1]

notes = get_dict()


class AudioSignal:
    def __init__(self, filepath: str, duration: float, offset: float, sample_override=None):

        # Read wavfile
        # Duration, offset, in seconds
        # sample_override=None for native sampling
        self.signal, self.sr = librosa.load(filepath, sr=sample_override, duration=duration, offset=offset)

        self.spectrum = Spectrum(self.signal, self.sr)


class Spectrum:
    def __init__(self, signal, samples):
        self.signal = signal
        self.sr = samples

        # Absolute value of complex conjugate from Fourier
        self.spectrum = np.absolute(np.fft.fft(self.signal))
        
        # Scipy signal peaks method
        # Distance = min distance between peaks, prominence = vertical min distance, threshold = general thresh
        f_bins = int(len(self.spectrum)*0.1)
        self.peaks, _ = find_peaks(self.spectrum[:f_bins], distance=10, prominence=100, threshold=1.1)

        self.freqs = []
        self.weights = []
        self.isolate(self.peaks)

    def plot_magnitude_spectrum(self, title, f_ratio=0.1):
        plt.figure(figsize=(18, 5))

        f = np.linspace(0, self.sr, len(self.spectrum))
        f_bins = int(len(self.spectrum)*f_ratio)


        plt.plot(self.peaks, self.spectrum[self.peaks], "xr")

        plt.plot(f[:f_bins], self.spectrum[:f_bins])
        plt.xlabel("Frequency (Hz)")
        plt.title(title)
        plt.show()

    def isolate(self, pks):
        conf, others = [], []

        for peak in pks:
            multiple = peak/pks[0]
            val = abs(multiple - round(multiple))
            
            if val < 0.02: conf.append(val)
            else: others.append(peak)
        
        if len(conf) > 2: 
            self.freqs.append(pks[0])
            self.weights.append(sum(self.spectrum[pks]))

        if len(others) != 0:
            self.isolate(others)


    def notes(self):
        # Funky one liner that turns the self.freqs array into an array of its closest entries in dict notes
        note_array = [min(notes, key=lambda x:abs(x - m)) for m in self.freqs]

        # Converts to the string key-value pair
        new_array = [notes[m] for m in note_array]

        print(new_array)





if __name__ == '__main__':
    audio = AudioSignal(violin_wav, duration=1.0, offset=float(0), sample_override=None)

    audio.spectrum.plot_magnitude_spectrum(title=f"{violin_wav} at time 0")
   
    print(audio.spectrum.weights)
    print(audio.spectrum.freqs)
    print(audio.spectrum.notes())
