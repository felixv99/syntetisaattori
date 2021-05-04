import sys
import pyaudio
import numpy as np
import threading
from oscillator import Oscillator
from adsr import EnvADSR
from scipy import signal
import math


class SoundOut:

    def __init__(self, gui_class):
        self.rate = 44100  # Sampling rate
        self.chunk_size = 1024  # Small piece from the wave
        self.low_pass_freq = 20000

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.rate, output=1,
                                  frames_per_buffer=self.chunk_size)
        self.stream.start_stream()

        self.period = self.chunk_size * self.rate
        self.chunk_move = 0  # Moves the wave forward

        self.amplitude = 0.03

        self.adsr = EnvADSR(self)
        self.osc = Oscillator()
        self.osc2 = Oscillator()
        self.gui_class = gui_class  # MainWindow class object

        self.key_playing = False

        t = threading.Thread(target=self.play_sound)
        t.start()

    def play_sound(self):

        while self.stream.is_active():  # Because while loop is running all the time, threading is needed
            wave = np.zeros(self.chunk_size)
            sos = signal.butter(4, self.low_pass_freq, output='sos', analog=False, fs=self.rate)  # Low-pass filter
            if self.key_playing:
                t = np.arange(self.chunk_move, self.chunk_move + self.chunk_size)
                adsr_value = self.adsr.get_adsr()
                if adsr_value <= 1 and self.amplitude <= 0.15:
                    wave = self.amplitude * adsr_value * (self.osc.get_wave(t) + self.osc2.get_wave(t))

                    # FOR PLOTTING THE SIGNAL
                    t2 = np.arange(0, 1024)
                    wave2 = self.amplitude * adsr_value * (self.osc.get_wave(t2) + self.osc2.get_wave(t2))
                    filtered2 = signal.sosfiltfilt(sos, wave2)
                    self.gui_class.get_canvas().plot(filtered2, t2)
                else:
                    wave = 0 * self.osc.get_wave(t)
                    print("Volume put to zero, you tried to use too loud volume")

            filtered = signal.sosfiltfilt(sos, wave)  # Filtering the signal
            self.stream.write(filtered.astype(np.float32).tobytes())

            if self.chunk_move == self.period:  # Prevents the wave part for going too high numbers
                self.chunk_move = 0
            self.chunk_move += self.chunk_size

    def get_osc(self):
        return self.osc

    def get_osc2(self):
        return self.osc2

    def get_adsr(self):
        return self.adsr

    def get_amplitude(self):
        return self.amplitude

    def change_amplitude(self, value):
        if value / 1000 <= 0.15:
            self.amplitude = (value / 1000)
        else:
            self.amplitude = 0

    def change_lowpass(self, value):
        if value < 100:
            self.low_pass_freq = 20000 - math.log10(value) * 10000
        else:
            self.low_pass_freq = 0.0001

    def key_state_change(self):  # Changes the state whether key is playing or not
        if self.key_playing == False:
            self.key_playing = True
            self.adsr.set_start_time()
            return True
        else:
            self.adsr.set_release_start_time()  # Changes the key_playing to false after the release phase is done
            return False

    def set_key_played_false(self):
        self.key_playing = False

    def is_key_played(self):
        return self.key_playing

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.chunk_move = 0


from PyQt5.QtWidgets import (QApplication, QPushButton, QFileDialog, QLabel)
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, QCoreApplication
from PyQt5.QtGui import *
from graphic import *
import os


# https://en.wikipedia.org/wiki/Piano_key_frequencies

class MainWindow(QtWidgets.QMainWindow):  # QtWidgets.QMainWindow #QDialog

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.synth = SoundOut(self)
        self.keys_held = []
        self.initUI()
        self.key_dict = {Qt.Key_A: 261.6256, Qt.Key_W: 277.1826, Qt.Key_S: 293.6648, Qt.Key_E: 311.1270,
                         Qt.Key_D: 329.6276, Qt.Key_F: 349.2282, Qt.Key_T: 369.9944, Qt.Key_G: 391.9954,
                         Qt.Key_Y: 415.3047, Qt.Key_H: 440.0000, Qt.Key_U: 466.1638, Qt.Key_J: 493.8833}

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(dir_path + "\images\knob.png"))
        self.setWindowTitle("Synthesizer by Felix")
        self.setStyleSheet(("background-color: #f3e6bc"))
        self.setGeometry(500, 500, 1000, 450)

        oscillator = self.synth.get_osc()
        oscillator2 = self.synth.get_osc2()

        self.wave_slider1 = WaveSlider(self, oscillator, 330, 85, 3, "wave1")
        self.octave_slider1 = OctaveSlider(self, oscillator, 210, 85, 1, "oct1")
        self.osc_vol1 = VolumeKnob(self, self.synth, 455, 120, 75, "VOL OSC1", 0.8)

        self.wave_slider2 = WaveSlider(self, oscillator2, 330, 280, 3, "wave2")
        self.octave_slider2 = OctaveSlider(self, oscillator2, 210, 280, 1, "oct2")
        self.osc_vol2 = VolumeKnob(self, self.synth, 455, 315, 75, "VOL OSC2", 0.8)

        self.attack = ADSRKnob(self, self.synth, 570, 70, 300, 30, "ATTACK")
        self.decay = ADSRKnob(self, self.synth, 670, 70, 300, 0, "DECAY")
        self.sustain = ADSRKnob(self, self.synth, 770, 70, 100, 100, "SUSTAIN")
        self.release = ADSRKnob(self, self.synth, 870, 70, 500, 30, "RELEASE")

        self.master_knob = VolumeKnob(self, self.synth, 50, 110, 30, "MASTER\nVOLUME", 1)
        self.low_pass_knob = LowPassKnob(self, self.synth)

        self.preset_name = QLabel('Init', self)
        self.preset_name.setGeometry(500, 0, 200, 30)
        self.preset_name.setStyleSheet('QLabel {background-color: #f3ecd6; color: #502c22; border: 1px solid #565a5e;}')
        self.preset_name.setAlignment(QtCore.Qt.AlignCenter)

        # FOR PLOTTING
        self.canvas = Plotter(self)
        self.canvas.move(585, 200)

    def initUI(self):
        save_preset_but = QPushButton('Save', self)
        save_preset_but.setStyleSheet('QPushButton {background-color: #b57956; color: #f3e6bc;}')
        save_preset_but.move(700, 0)
        save_preset_but.clicked.connect(self.save_preset)

        load_preset_but = QPushButton('Load', self)
        load_preset_but.setStyleSheet('QPushButton {background-color: #b57956; color: #f3e6bc;}')
        load_preset_but.move(800, 0)
        load_preset_but.clicked.connect(self.load_preset)

        exit_button = QPushButton('Exit', self)
        exit_button.clicked.connect(self.activate_close)
        exit_button.setStyleSheet('QPushButton {background-color: #b57956; color: #f3e6bc;}')

        self.app.aboutToQuit.connect(self.activate_close)

    def save_preset(self):
        option = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(self, "Save preset", "", "*.csv", options=option)
        if filename[0] != '':
            data = open(filename[0], 'w')
            saver = ["MasterVolumeKnob," + str(self.master_knob.get_value()) + '\n',
                     "OscOctaveSlider1," + str(self.octave_slider1.get_value()) + '\n',
                     "OscWaveSlider1," + str(self.wave_slider1.get_value()) + '\n',
                     "OscOctaveSlider2," + str(self.octave_slider2.get_value()) + '\n',
                     "OscWaveSlider2," + str(self.wave_slider2.get_value()) + '\n'
                     "Attack," + str(self.attack.get_value()) + '\n',
                     "Decay," + str(self.decay.get_value()) + '\n',
                     "Sustain," + str(self.sustain.get_value()) + '\n',
                     "Release," + str(self.release.get_value()) + '\n',
                     "OscVol1," + str(self.osc_vol1.get_value()) + '\n',
                     "OscVol2," + str(self.osc_vol2.get_value()) + '\n',
                     "LowPass," + str(self.low_pass_knob.get_value()) + '\n']
            data.writelines(saver)
            data.close()

            name = os.path.basename(filename[0])
            name = name.split('.')
            self.preset_name.setText(str(name[0]))
            print("Preset " + str(name[0]) + " saved")

    def load_preset(self):
        option = QFileDialog.Options()
        filename = QFileDialog.getOpenFileName(self, "Open preset", "", "*.csv", options=option)
        if filename[0] != '':
            data = open(filename[0], 'r')
            preset_list = []
            for row in data:
                row = row.rstrip()
                row = row.split(',')
                preset_list.append(row[1])
            data.close()
            if len(preset_list) == 12:
                self.master_knob.load_value(int(preset_list[0]))
                self.octave_slider1.load_value(int(preset_list[1]))
                self.wave_slider1.load_value(int(preset_list[2]))
                self.octave_slider2.load_value(int(preset_list[3]))
                self.wave_slider2.load_value(int(preset_list[4]))
                self.attack.load_value(int(preset_list[5]))
                self.decay.load_value(int(preset_list[6]))
                self.sustain.load_value(int(preset_list[7]))
                self.release.load_value(int(preset_list[8]))
                self.osc_vol1.load_value(int(preset_list[9]))
                self.osc_vol2.load_value(int(preset_list[10]))
                self.low_pass_knob.load_value(int(preset_list[11]))

                name = os.path.basename(filename[0])
                name = name.split('.')
                self.preset_name.setText(str(name[0]))
                print("Preset " + str(name[0]) + " loaded")
            else:
                print("Invalid preset file detected")


    @pyqtSlot()
    def activate_close(self):
        print("Exited the synthesizer")
        self.synth.close_stream()
        QCoreApplication.quit()
        sys.exit()

    def keyPressEvent(self, event):

        if event.isAutoRepeat():
            pass
        else:
            if event.key() in self.key_dict:
                if not self.keys_held:
                    self.synth.key_state_change()
                    self.keys_held.append(event.key())
                else:
                    self.keys_held.clear()
                    self.keys_held.append(event.key())

                self.synth.get_adsr().one_key_at_once()  # Fixes pressing another key while release phase is still going

                if self.synth.is_key_played() == True:
                    self.synth.get_adsr().set_start_time()
                    self.synth.get_osc().change_freq(self.key_dict[event.key()])
                    self.synth.get_osc2().change_freq(self.key_dict[event.key()])

    def keyReleaseEvent(self, event):

        if event.isAutoRepeat():
            pass
        else:
            if event.key() in self.key_dict:
                if event.key() in self.keys_held:
                    self.synth.key_state_change()
                    self.keys_held.remove(event.key())

    def get_canvas(self):
        return self.canvas

    # Functions for synth_test.py
    def get_synth(self):
        return self.synth

    def get_master_knob(self):
        return self.master_knob

    def get_osc_vol1(self):
        return self.osc_vol1

    def get_osc_vol2(self):
        return self.osc_vol2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = MainWindow(app)
    scene.show()
    sys.exit(app.exec_())
