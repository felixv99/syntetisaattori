import sys
import pyaudio
import numpy as np
import threading

from PyQt5.QtCore import pyqtSlot, QCoreApplication
from scipy import signal
import time
import threading


# SIN FORMULA y = A * sin(((2*pi*f)/rate)*T)

class SoundOut:  # Ensimmäinen sinisignaali ääni ulos taajuudella 440 painamalla A näppäintä

    def __init__(self):
        self.rate = 44100
        self.chunk_size = 1024  # Small piece from the wave
        self.amplitude = 0.3
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.rate, output=1,
                                  frames_per_buffer=self.chunk_size)
        self.stream.start_stream()

        self.period = self.chunk_size * self.rate
        self.chunk_move = 0  # Moves the wave forward
        self.freq_hz = 440.0
        self.key_played = False
        t = threading.Thread(target=self.play_sound)
        t.start()

    def play_sound(self):

        while self.stream.is_active():  # Because while loop is running all the time, threading is needed
            t = np.arange(self.chunk_move, self.chunk_move + self.chunk_size)
            wave = self.amplitude * np.sin(((2 * np.pi * self.freq_hz) / self.rate) * t)
            if self.key_played:
                self.stream.write(wave.astype(np.float32).tostring())
            if self.chunk_move == self.period:  # Prevents wave part for going way too big numbers
                self.chunk_move = 0
            self.chunk_move += self.chunk_size
            # print("1")

    """
    def stream_state(self):
        return self.stream

    def p_state(self):
        return self.p
    """

    def close_stream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.chunk_move = 0

    def state(self):  # Changes the state wheter key is playing or not
        if self.key_played == False:
            self.key_played = True
            print("True")
            return True
        else:
            self.key_played = False
            print("False")
            return False


from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton)
from PyQt5.Qt import Qt


class ButtonPress(QWidget):

    def __init__(self, synth):
        super().__init__()
        # self.initUI()
        # self.player = 0
        self.synth = synth
        self.initUI()

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
            state = self.synth.state()
            if event.key() == Qt.Key_A:
                if state == False:
                    # print("press")
                    self.synth.play_sound()

        """
        if event.isAutoRepeat():
            pass
        else:
            state = self.synth.state()
            if event.key() == Qt.Key_A and state is False:
                print("press")
                self.synth.play_sound()
            elif event.key() == Qt.Key_A and state is True:
                self.synth.close_stream()


        """

    def keyReleaseEvent(self, event):

        if event.isAutoRepeat():
            pass
        else:
            state = self.synth.state()
            # if state == True:
            # self.synth.close_stream()
            # print("released")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    synth = SoundOut()
    press = ButtonPress(synth)
    press.show()
    sys.exit(app.exec_())