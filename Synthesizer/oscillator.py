from scipy import signal
import numpy as np


class Oscillator:
    def __init__(self):
        self.rate = 44100
        self.freq_hz = 0
        self.octave = 1
        self.wave_type = np.sin
        self.amplitude = 0.5

    def change_wave(self, value):
        if value == 1:
            self.wave_type = signal.sawtooth
        elif value == 2:
            self.wave_type = signal.square
        elif value == 3:
            self.wave_type = np.sin

    def change_octave(self, value):
        if value == 0:
            self.octave = 0.5
        elif value == 1:
            self.octave = 1
        elif value == 2:
            self.octave = 2
        elif value == 3:
            self.octave = 4
        elif value == -1:
            self.octave = 0.5*0.5

    def get_wave(self, t):  # WAVE FORMULA y = A * WAVE_TYPE(((2*pi*f)/rate)*T)
        if self.amplitude <= 1:
            wave = self.amplitude*self.wave_type(((2 * np.pi * (self.octave * self.freq_hz)) / self.rate) * t)
        else:
            wave = 0 * self.wave_type(((2 * np.pi * (self.octave * self.freq_hz)) / self.rate) * t)
            print("Volume put to zero, you tried to use too loud volume")
        return wave

    def change_freq(self, changed_freq):
        self.freq_hz = changed_freq

    def get_amplitude(self):
        return self.amplitude

    def change_amplitude(self, value):
        if value / 150 <= 1:
            self.amplitude = (value / 150)
        else:
            self.amplitude = 0
