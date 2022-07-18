import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import numpy as np
import wave
from scipy.io import wavfile
from scipy.signal import find_peaks

violin_wav = "samples/violin_c.wav"
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
        
        # Scipy signal peaks method
        # Distance = min distance between peaks, prominence = vertical min distance, threshold = general thresh
        f_bins = int(len(self.spectrum)*0.1)
        self.peaks, _ = find_peaks(self.spectrum[:f_bins], distance=30, prominence=10, threshold=0.9)

    def plot_magnitude_spectrum(self, title, f_ratio=0.1):
        plt.figure(figsize=(18, 5))

        f = np.linspace(0, self.sr, len(self.spectrum))
        f_bins = int(len(self.spectrum)*f_ratio)


        plt.plot(self.peaks, self.spectrum[self.peaks], "xr")

        plt.plot(f[:f_bins], self.spectrum[:f_bins])
        plt.xlabel("Frequency (Hz)")
        plt.title(title)
        plt.show()


if __name__ == '__main__':
    audio = AudioSignal(violin_wav, duration=1.0, offset=float(1), sample_override=None)

    audio.spectrum.plot_magnitude_spectrum(title=f"{violin_wav} at time 0")

    print(audio.spectrum.peaks / audio.spectrum.peaks[0])
