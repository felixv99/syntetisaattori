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

    def __init__(self):
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

from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton)
from PyQt5.Qt import Qt
from PyQt5 import QtWidgets
from graphic import WaveSlider, OctaveSlider, VolumeKnob, ADSRKnob

# https://en.wikipedia.org/wiki/Piano_key_frequencies


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, synth):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget())
        # self.initUI()
        # self.player = 0
        self.keys_held = []
        self.synth = synth
        self.initUI()
        self.key_dict = {Qt.Key_A: 261.6256, Qt.Key_W: 277.1826, Qt.Key_S: 293.6648, Qt.Key_E: 311.1270,
                         Qt.Key_D: 329.6276, Qt.Key_F: 349.2282, Qt.Key_T: 369.9944, Qt.Key_G: 391.9954,
                         Qt.Key_Y: 415.3047, Qt.Key_H: 440.0000, Qt.Key_U: 466.1638, Qt.Key_J: 493.8833}
        oscillator = self.synth.get_osc()
        oscillator2 = self.synth.get_osc2()
        WaveSlider(self, oscillator, 330, 70, 3)
        OctaveSlider(self, oscillator, 210, 70, 1)
        WaveSlider(self, oscillator2, 330, 280, 3)
        OctaveSlider(self, oscillator2, 210, 280, 1)
        VolumeKnob(self, synth)
        #ADSRKnob(self, oscillator, "ATTACK")
        ADSRKnob(self, synth, 570, 70, 500, 30, "ATTACK")
        ADSRKnob(self, synth, 670, 70, 300, 0, "DECAY")
        #ADSRKnob(self, oscillator, 770, 70, 150, 150, "SUSTAIN")
        ADSRKnob(self, synth, 770, 70, 100, 100, "SUSTAIN")
        ADSRKnob(self, synth, 870, 70, 500, 30, "RELEASE")
        # ADSRKnob2(self, oscillator)

        self.setGeometry(500, 500, 800, 500)

    def initUI(self):
        self.__button = QPushButton('Exit', self)
        self.__button.clicked.connect(self.activate_close)
        self.show()

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
    synth = SoundOut()
    scene = MainWindow(synth)
    scene.show()
    sys.exit(app.exec_())
