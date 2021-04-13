import sys
import pyaudio
import numpy as np
import time
from PyQt5.QtCore import pyqtSlot, QCoreApplication
import threading
from oscillator import Oscillator
from adsr import EnvADSR


# SIN FORMULA y = A * sin(((2*pi*f)/rate)*T)

class SoundOut:

    def __init__(self, gui_class):
        self.rate = 44100
        self.chunk_size = 1024  # Small piece from the wave
        #self.amplitude = 0.3
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.rate, output=1,
                                  frames_per_buffer=self.chunk_size)
        self.stream.start_stream()

        self.period = self.chunk_size * self.rate
        self.chunk_move = 0  # Moves the wave forward
        self.amplitude = 0.03
        self.adsr = EnvADSR(self)
        self.key_playing = False
        self.key_stop = True
        self.osc = Oscillator()
        self.osc2 = Oscillator()

        self.gui_class = gui_class

        t = threading.Thread(target=self.play_sound)
        t.start()

    def play_sound(self):

        while self.stream.is_active():  # Because while loop is running all the time, threading is needed
            wave = np.zeros(self.chunk_size)
            if self.key_playing:
                t = np.arange(self.chunk_move, self.chunk_move + self.chunk_size)

                adsr_value = self.adsr.get_adsr()
                if adsr_value <= 1 and self.amplitude <= 0.15:
                    wave = self.amplitude*adsr_value*(self.osc.get_wave(t)+self.osc2.get_wave(t))

                    # FOR PLOTTING THE SIGNAL
                    t2 = np.arange(0, 1024)
                    wave2 = self.amplitude*adsr_value*(self.osc.get_wave(t2)+self.osc2.get_wave(t2))
                    self.gui_class.get_canvas().plot(wave2, t2)
                else:
                    wave = 0*self.osc.get_wave(t)
            self.stream.write(wave.astype(np.float32).tostring())
            if self.chunk_move == self.period:  # Prevents wave part for going way too big numbers
                self.chunk_move = 0
            self.chunk_move += self.chunk_size
            # print("1")

    def get_osc(self):
        return self.osc

    def get_osc2(self):
        return self.osc2

    def get_adsr(self):
        return self.adsr

    def get_amplitude(self):
        return self.amplitude

    def change_amplitude(self, value):
        self.amplitude = (value / 1000)

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.chunk_move = 0


    def key_state_change(self):  # Changes the state wheter key is playing or not
        if self.key_playing == False:
            self.key_playing = True
            #self.osc.start_adsr_time()
            #if self.adsr.get_adsr_tail() == True:
                #self.adsr.one_key_at_once()
            self.adsr.set_start_time()
            # print("True")
            return True
        else:
            #self.key_playing = False
            self.adsr.set_release_start_time()
            # print("False")
            return False

    def set_key_played_false(self):
        self.key_playing = False

    def is_key_played(self):
        return self.key_playing

from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QVBoxLayout, QFileDialog, QMainWindow, QLabel, QToolBar,
                             QToolButton, QAction)
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from graphic import WaveSlider, OctaveSlider, VolumeKnob, ADSRKnob, Plotter
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import os

# https://en.wikipedia.org/wiki/Piano_key_frequencies

class MainWindow(QtWidgets.QMainWindow): #QtWidgets.QMainWindow #QDialog

    def __init__(self):
        super().__init__()
        synth = SoundOut(self)
        self.setCentralWidget(QtWidgets.QWidget())
        self.keys_held = []
        self.synth = synth
        self.initUI()
        self.key_dict = {Qt.Key_A: 261.6256, Qt.Key_W: 277.1826, Qt.Key_S: 293.6648, Qt.Key_E: 311.1270,
                         Qt.Key_D: 329.6276, Qt.Key_F: 349.2282, Qt.Key_T: 369.9944, Qt.Key_G: 391.9954,
                         Qt.Key_Y: 415.3047, Qt.Key_H: 440.0000, Qt.Key_U: 466.1638, Qt.Key_J: 493.8833}

        oscillator = self.synth.get_osc()
        oscillator2 = self.synth.get_osc2()
        self.setWindowIcon(QtGui.QIcon('knob.png'))
        self.setWindowTitle("Synthesizer by Felix")
        self.wave_slider1 = WaveSlider(self, oscillator, 330, 85, 3)
        self.octave_slider1 = OctaveSlider(self, oscillator, 210, 85, 1)

        self.wave_slider2 = WaveSlider(self, oscillator2, 330, 280, 3)
        self.octave_slider2 = OctaveSlider(self, oscillator2, 210, 280, 1)

        self.master_knob = VolumeKnob(self, synth, 50, 180, 30, "MASTER\nVOLUME", 1)
        self.osc_vol1 = VolumeKnob(self, synth, 450, 120, 0, "VOL OSC1", 0.8)
        self.osc_vol2 = VolumeKnob(self, synth, 450, 315, 0, "VOL OSC2", 0.8)

        self.attack = ADSRKnob(self, synth, 570, 70, 500, 30, "ATTACK")
        self.decay = ADSRKnob(self, synth, 670, 70, 300, 0, "DECAY")
        self.sustain = ADSRKnob(self, synth, 770, 70, 100, 100, "SUSTAIN")
        self.release = ADSRKnob(self, synth, 870, 70, 500, 30, "RELEASE")

        self.setGeometry(500, 500, 1000, 450)
        #self.setStyleSheet("background-color:lightgray")

        self.preset_name = QLabel('Init', self)
        self.preset_name.setGeometry(500, 1, 200, 28)
        self.preset_name.setStyleSheet(("background-color: lightgray"))
        self.preset_name.setAlignment(QtCore.Qt.AlignCenter)

         #FOR PLOTTING
        self.canvas = Plotter(self)
        self.canvas.move(585, 200)

    def initUI(self):
        self.__button = QPushButton('Exit', self)
        self.__button.clicked.connect(self.activate_close)

        save_preset_but = QPushButton('Save', self)
        save_preset_but.move(700, 0)
        save_preset_but.clicked.connect(self.save_preset)

        #save_preset_but.setWindowIcon(QtGui.QIcon('./knob.png'))
        #save_preset_but.setIconSize(QtCore.QSize(130, 130))

        load_preset_but = QPushButton('Load', self)
        load_preset_but.move(800, 0)
        load_preset_but.clicked.connect(self.load_preset)

        #self.show()

    def save_preset(self):
        option = QFileDialog.Options()
        filename = QFileDialog.getSaveFileName(self, "Save preset", "", "*.csv", options=option) #"All Files (*)"
        #if not file:
        #print(filename)
        #print(filename[0])
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
                     "OscVol2," + str(self.osc_vol2.get_value()) + '\n']
            data.writelines(saver)
            data.close()

            name = os.path.basename(filename[0])
            name = name.split('.')
            self.preset_name.setText(str(name[0]))
            print("Preset "+str(name[0])+" saved")

    def load_preset(self):
        option = QFileDialog.Options()
        filename = QFileDialog.getOpenFileName(self, "Open preset", "", "*.csv", options=option)  # "All Files (*)"
        if filename[0] != '':
            data = open(filename[0], 'r')
            #print(data.read())
            preset_list = []
            for row in data:
                row = row.rstrip()
                row = row.split(',')
                preset_list.append(row[1])
            data.close()
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

            name = os.path.basename(filename[0])
            name = name.split('.')
            self.preset_name.setText(str(name[0]))
            print("Preset "+str(name[0])+" loaded")

    def get_canvas(self):
        return self.canvas

    @pyqtSlot()
    def activate_close(self):  # Ohjelma ei sulkeudu kokonaan äxästä, mutta erillisestä napista kyllä
        self.__button.clicked.connect(self.close)
        self.synth.close_stream()
        QCoreApplication.quit()


    def keyPressEvent(self, event):

        if event.isAutoRepeat():
            pass
        else:
            """
            if event.key() == Qt.Key_A: # Qt.Key_A
                state = self.synth.state()
                # print(event.key())
                if state:
                    # print("press")
                    self.synth.change_freq(261.6256)
                    print(self.synth.get_freq())
                    #self.synth.play_sound()
            """
            if event.key() in self.key_dict:
                if not self.keys_held:
                    self.synth.key_state_change()
                    self.keys_held.append(event.key())
                else:
                    self.keys_held.clear()
                    self.keys_held.append(event.key())
                self.synth.get_adsr().one_key_at_once() # Fixes Pressing another key while release phase is still going
                if self.synth.is_key_played() == True:
                    #self.synth.change_freq(self.key_dict[event.key()])
                    #self.synth.change_key_stop()
                    self.synth.get_osc().change_freq(self.key_dict[event.key()])    #Tutki sanakirjaan True ja Falsen laittamista eri nuottien kohdalle
                    self.synth.get_osc2().change_freq(self.key_dict[event.key()])

    def keyReleaseEvent(self, event):

        if event.isAutoRepeat():
            pass
        else:
            """
            if event.key() == Qt.Key_A:
                print("na aa")
                state = self.synth.state()
                # if state == True:
                # self.synth.close_stream()
                # print("released")
            """
            if event.key() in self.key_dict:
                # self.synth.get_osc().start_adsr_release_time()
                # print(self.synth.get_osc().get_adsr().get_release_time())
                # time.sleep(self.synth.get_osc().get_adsr().get_release_time())
                #if self.synth.is_key_played() == True:
                if event.key() in self.keys_held:
                    state = self.synth.key_state_change()
                    self.keys_held.remove(event.key())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = MainWindow()
    scene.show()
    sys.exit(app.exec_())
