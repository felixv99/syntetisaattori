from scipy import signal
import numpy as np
# from adsr import EnvADSR

class Oscillator:
    def __init__(self):
        self.rate = 44100
        self.freq_hz = 0
        #self.amplitude = 0.03
        self.octave = 1
        self.wave_type = np.sin
        #self.adsr = EnvADSR(soundout)

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
    '''
    def change_amplitude(self, value):
        old_amp = self.amplitude
        self.amplitude = (value / 1000)
        #self.adsr.change_sustain_with_amplitude(self.amplitude / old_amp)
        print(self.amplitude)
    '''
    '''
    def start_adsr_time(self):
        self.adsr.set_start_time()

    def start_adsr_release_time(self):
        self.adsr.set_release_start_time()
    
    def get_adsr(self):
        return self.adsr
    '''

    def get_wave(self, t):
        wave = self.wave_type(((2 * np.pi * (self.octave * self.freq_hz)) / self.rate) * t)
        return wave

    def change_freq(self, changed_freq):
        self.freq_hz = changed_freq
        #print("FREQ CHANGED")