from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QDial)
from PyQt5.QtCore import Qt
import numpy as np


class WaveSlider(QSlider):

    def __init__(self, parent, oscillator, location_x, location_y, set_value):
        super(WaveSlider, self).__init__(parent)
       # wave_slider = QSlider(Qt.Horizontal, self)
        #wave_slider.setGeometry(30, 40, 200, 30)
        #wave_slider.valueChanged[int].connect(self.changeValue)
        self.setGeometry(location_x, location_y, 40, 120)
        self.setMinimum(1)
        self.setMaximum(3)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setSliderPosition(set_value)
        self.valueChanged.connect(self.change_value)
        sin_label = QLabel(parent)
        sin_label.setText("SIN")
        sin_label.setGeometry(location_x + 35, location_y - 45, 100, 100)
        sin_label.show()
        square_label = QLabel(parent)
        square_label.setText("SQUARE")
        square_label.setGeometry(location_x + 35, location_y + 10, 100, 100)
        square_label.show()
        saw_label = QLabel(parent)
        saw_label.setText("SAW")
        saw_label.setGeometry(location_x + 35, location_y + 65, 100, 100)
        saw_label.show()
        wave_label = QLabel(parent)
        wave_label.setText("WAVE")
        wave_label.setGeometry(location_x + 35, location_y - 70, 100, 100)
        wave_label.show()
        self.show()
        self.osc = oscillator


    def change_value(self, value):
        self.osc.change_wave(value)
        print(value)


class OctaveSlider(QSlider):

    def __init__(self, parent, osc,location_x, location_y, set_value):
        super(OctaveSlider, self).__init__(parent)
        self.setGeometry(location_x, location_y, 40, 120)
        self.setMinimum(-1)
        self.setMaximum(3)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setSliderPosition(set_value)
        self.valueChanged.connect(self.change_value)
        oct_label = QLabel(parent)
        oct_label.setText("OCTAVE")
        oct_label.setGeometry(location_x, location_y - 70, 100, 100)
        oct_label.show()
        self.show()
        self.osc = osc

    def change_value(self, value):
        self.osc.change_octave(value)
        #print(value)


class VolumeKnob(QDial):

    def __init__(self, parent, soundout):
        super(VolumeKnob, self).__init__(parent)
        self.setGeometry(50, 180, 80, 80)
        self.setMinimum(0)
        self.setMaximum(150)
        #self.setTickPosition(QSlider.TicksBelow)
        #self.setTickInterval(1)
        self.setValue(30)
        self.valueChanged.connect(self.change_value)
        vol_label = QLabel(parent)
        vol_label.setText("MASTER\nVOLUME")
        vol_label.setGeometry(65, 110, 100, 100)
        vol_label.show()
        self.show()
        self.soundout = soundout

    def change_value(self, value):
        self.soundout.change_amplitude(value)
        print(value)


class ADSRKnob(QDial):

    def __init__(self, parent, soundout, location_x, location_y, set_max, set_value, adsr_type):
        super(ADSRKnob, self).__init__(parent)
        self.setGeometry(location_x, location_y, 80, 80)
        self.setMinimum(0)
        self.setMaximum(set_max)
        #self.setTickPosition(QSlider.TicksBelow)
        #self.setTickInterval(1)
        self.setValue(set_value)
        self.valueChanged.connect(lambda i: self.change_value(i, adsr_type))
        vol_label = QLabel(parent)
        vol_label.setText(adsr_type)
        vol_label.setGeometry(location_x + 15, 15, 100, 100)
        vol_label.show()
        self.show()
        self.adsr = soundout.get_adsr()


    def change_value(self, value, type_is):
        #self.adsr.change_attack_time(value)
        self.adsr.change_adsr_knobs(value, type_is)


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt


class Plotter(FigureCanvas):

    def __init__(self, parent):
        self.fig, ax = plt.subplots(figsize=(5, 3),dpi=70)
        super().__init__(self.fig)
        self.setParent(parent)

        ax.set_xticks([])
        ax.set_xticklabels([])
        ax.set_yticks([])
        ax.set_yticklabels([])

        #ax.spines['top'].set_visible(False)
        #ax.spines['right'].set_visible(False)
        #ax.spines['bottom'].set_visible(False)
        #ax.spines['left'].set_visible(False)

        self.fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)

        wave = np.zeros(1024)
        t = np.arange(0, 1024)
        self.plot_info, = ax.plot(t, wave, 'b-')
        plt.ion()

    def plot(self, wave, t):
        self.plot_info.set_xdata(t)
        self.plot_info.set_ydata(0.25*wave)
        #print(wave)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

