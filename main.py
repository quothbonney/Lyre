import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import numpy as np
import wave
from scipy.io import wavfile

violin_wav = "samples/chords.wav"
sax_wav = "samples/sax.wav"


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


    def plot_magnitude_spectrum(self, title, f_ratio=0.1):
        plt.figure(figsize=(18, 5))

        f = np.linspace(0, self.sr, len(self.spectrum))
        f_bins = int(len(self.spectrum)*f_ratio)

        plt.plot(f[:f_bins], self.spectrum[:f_bins])
        plt.xlabel("Frequency (Hz)")
        plt.title(title)
        plt.show()


if __name__ == '__main__':
    for i in range(10):
        audio = AudioSignal(violin_wav, duration=1.0, offset=float(i), sample_override=10000)

        audio.spectrum.plot_magnitude_spectrum(title=f"{violin_wav} at time {i}")
