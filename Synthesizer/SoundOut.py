import sys
import pyaudio
import numpy as np

from PyQt5.QtCore import pyqtSlot, QCoreApplication
import threading
from oscillator import Oscillator


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
        #self.freq_hz = 0
        self.key_playing = False
        self.osc = Oscillator(self)
        t = threading.Thread(target=self.play_sound)
        t.start()

    def play_sound(self):

        while self.stream.is_active():  # Because while loop is running all the time, threading is needed
            wave = np.zeros(self.chunk_size)
            if self.key_playing:
                t = np.arange(self.chunk_move, self.chunk_move + self.chunk_size)
                #wave = self.amplitude * np.sin(((2 * np.pi * self.freq_hz) / self.rate) * t)
                wave = self.osc.get_wave(t)
            self.stream.write(wave.astype(np.float32).tostring())
            if self.chunk_move == self.period:  # Prevents wave part for going way too big numbers
                self.chunk_move = 0
            self.chunk_move += self.chunk_size
            # print("1")

    def get_osc(self):
        return self.osc

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.chunk_move = 0

    def key_state_change(self):  # Changes the state wheter key is playing or not
        if self.key_playing == False:
            self.key_playing = True
            self.osc.start_adsr_time()
            # print("True")
            return True
        else:
            self.key_playing = False
            # print("False")
            return False

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
        self.synth = synth
        self.initUI()
        self.key_dict = {Qt.Key_A: 261.6256, Qt.Key_W: 277.1826, Qt.Key_S: 293.6648, Qt.Key_E: 311.1270,
                         Qt.Key_D: 329.6276, Qt.Key_F: 349.2282, Qt.Key_T: 369.9944, Qt.Key_G: 391.9954,
                         Qt.Key_Y: 415.3047, Qt.Key_H: 440.0000, Qt.Key_U: 466.1638, Qt.Key_J: 493.8833}
        self.wave_slider = WaveSlider(self, synth)
        oscillator = self.synth.get_osc()
        self.octave_slider = OctaveSlider(self, oscillator)
        VolumeKnob(self, oscillator)
        ADSRKnob(self, oscillator)
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
                state = self.synth.key_state_change()
                if state:
                    #self.synth.change_freq(self.key_dict[event.key()])
                    self.synth.get_osc().change_freq(self.key_dict[event.key()])

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
                state = self.synth.key_state_change()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    synth = SoundOut()
    scene = MainWindow(synth)
    scene.show()
    sys.exit(app.exec_())
