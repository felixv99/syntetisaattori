from PyQt5.QtWidgets import (QSlider, QLabel, QDial)
from PyQt5.QtCore import Qt
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class WaveSlider(QSlider):

    def __init__(self, parent, oscillator, location_x, location_y, set_value, osc_type):
        super(WaveSlider, self).__init__(parent)
        self.setGeometry(location_x, location_y, 40, 120)
        self.setMinimum(1)
        self.setMaximum(3)
        self.setTickInterval(1)
        self.setSliderPosition(set_value)
        self.valueChanged.connect(self.change_value)

        if osc_type == "wave1":
            self.setStyleSheet("QSlider::groove:vertical {background: #f3e3ae; border: 1px solid #565a5e; height: "
                               "118; width: 15; margin: 0px; border-radius: 4px;} QSlider::handle:vertical {"
                               "background: #f5886b; border: 1px solid #565a5e; width: 24px; height: 39px; "
                               "border-radius: 4px;}")
        elif osc_type == "wave2":
            self.setStyleSheet("QSlider::groove:vertical {background: #f3e3ae; border: 1px solid #565a5e; height: "
                               "118; width: 15; margin: 0px; border-radius: 4px;} QSlider::handle:vertical {"
                               "background: #72ae95; border: 1px solid #565a5e; width: 24px; height: 39px; "
                               "border-radius: 4px;}")

        sin_label = QLabel(parent)
        sin_label.setText("SIN")
        sin_label.setGeometry(location_x + 35, location_y + 12, 30, 15)
        sin_label.setStyleSheet("color:#502c22")
        sin_label.show()

        square_label = QLabel(parent)
        square_label.setText("SQUARE")
        square_label.setGeometry(location_x + 35, location_y + 52, 50, 15)
        square_label.setStyleSheet("color:#502c22")
        square_label.show()

        saw_label = QLabel(parent)
        saw_label.setText("SAW")
        saw_label.setStyleSheet("color:#502c22")
        saw_label.setGeometry(location_x + 35, location_y + 90, 30, 15)
        saw_label.show()

        wave_label = QLabel(parent)
        wave_label.setText("WAVE")
        wave_label.setGeometry(location_x + 15, location_y - 25, 55, 15)
        wave_label.setStyleSheet("color:#502c22")
        wave_label.show()

        self.osc = oscillator

    def change_value(self, value):
        self.osc.change_wave(value)

    def get_value(self):
        return self.value()

    def load_value(self, value):
        self.setValue(value)


class OctaveSlider(QSlider):

    def __init__(self, parent, osc, location_x, location_y, set_value, osc_type):
        super(OctaveSlider, self).__init__(parent)
        self.setGeometry(location_x, location_y, 40, 120)
        self.setMinimum(-1)
        self.setMaximum(3)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setSliderPosition(set_value)
        self.valueChanged.connect(self.change_value)
        self.setStyleSheet("color: #72ae95")

        oct_label = QLabel(parent)
        oct_label.setText("OCTAVE")
        oct_label.setGeometry(location_x, location_y - 25, 55, 15)
        oct_label.setStyleSheet("color:#502c22")
        oct_label.show()

        self.osc = osc

        if osc_type == "oct1":
            self.setStyleSheet("QSlider::groove:vertical {background: #f3e3ae; border: 1px solid #565a5e; height: "
                               "118; width: 15; margin: 0px; border-radius: 4px;} QSlider::handle:vertical {"
                               "background: #f5886b; border: 1px solid #565a5e; width: 24px; height: 20px; "
                               "border-radius: 4px;}")
        elif osc_type == "oct2":
            self.setStyleSheet("QSlider::groove:vertical {background: #f3e3ae;border: 1px solid #565a5e; height: 118; "
                               "width: 15; margin: 0px; border-radius: 4px;} QSlider::handle:vertical {background: "
                               "#72ae95; border: 1px solid #565a5e; width: 24px; height: 20px; border-radius: 4px;}")

    def change_value(self, value):
        self.osc.change_octave(value)

    def get_value(self):
        return self.value()

    def load_value(self, value):
        self.setValue(value)


class VolumeKnob(QDial):

    def __init__(self, parent, soundout, location_x, location_y, set_value, volume_type, size):
        super(VolumeKnob, self).__init__(parent)
        self.setGeometry(location_x, location_y, 80*size, 80*size)
        self.setMinimum(0)
        self.setMaximum(150)
        self.setValue(set_value)
        self.valueChanged.connect(self.change_value)

        vol_label = QLabel(parent)
        vol_label.setText(volume_type)
        vol_label.setGeometry(location_x, location_y - 30, 70, 28)
        vol_label.setStyleSheet("color:#502c22")
        vol_label.setAlignment(Qt.AlignCenter)
        vol_label.show()

        self.soundout = soundout
        self.volume_type = volume_type

        if volume_type == "VOL OSC2":
            self.setStyleSheet("background-color: #72ae95")
        elif volume_type == "VOL OSC1":
            self.setStyleSheet("background-color: #f5886b")
        elif volume_type == "MASTER\nVOLUME":
            self.setStyleSheet("background-color: #5a3d2b")

    def change_value(self, value):
        if self.volume_type == "MASTER\nVOLUME":
            self.soundout.change_amplitude(value)
        elif self.volume_type == "VOL OSC1":
            self.soundout.get_osc().change_amplitude(value)
        elif self.volume_type == "VOL OSC2":
            self.soundout.get_osc2().change_amplitude(value)

    def get_value(self):
        return self.value()

    def load_value(self, value):
        self.setValue(value)


class ADSRKnob(QDial):

    def __init__(self, parent, soundout, location_x, location_y, set_max, set_value, adsr_type):
        super(ADSRKnob, self).__init__(parent)
        self.setGeometry(location_x, location_y, 80, 80)
        self.setMinimum(0)
        self.setMaximum(set_max)
        self.setValue(set_value)
        self.valueChanged.connect(lambda i: self.change_value(i, adsr_type))

        adsr_label = QLabel(parent)
        adsr_label.setText(adsr_type)
        adsr_label.setGeometry(location_x + 12, 55, 55, 15)
        adsr_label.setAlignment(Qt.AlignCenter)
        adsr_label.setStyleSheet("color:#502c22")
        adsr_label.show()

        self.adsr = soundout.get_adsr()

        self.setStyleSheet(("background-color: #f1c972"))

    def change_value(self, value, type_is):
        self.adsr.change_adsr_knobs(value, type_is)

    def get_value(self):
        return self.value()

    def load_value(self, value):
        self.setValue(value)


class Plotter(FigureCanvas):

    def __init__(self, parent):
        self.fig, self.ax = plt.subplots(figsize=(5, 3), dpi=70)
        super().__init__(self.fig)
        self.setParent(parent)

        self.ax.set_xticks([])
        self.ax.set_xticklabels([])
        self.ax.set_yticks([])
        self.ax.set_yticklabels([])

        self.fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)
        self.fig.patch.set_facecolor('#f3e6bc')

        wave = np.zeros(1024)
        t = np.arange(0, 1024)

        self.plot_info, = self.ax.plot(t, wave, color='#502c22')
        self.ax.set_facecolor("#f3ecd6")
        plt.ion()

    def plot(self, wave, t):
        self.plot_info.set_xdata(t)
        self.plot_info.set_ydata(0.25*wave)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class LowPassKnob(QDial):
    def __init__(self, parent, soundout):
        super(LowPassKnob, self).__init__(parent)
        self.setGeometry(50, 300, 80, 80)
        self.setMinimum(-85)  # when -85<value<-100 sound starts to distort
        self.setMaximum(-1)
        self.setValue(100)
        self.valueChanged.connect(self.change_value)

        vol_label = QLabel(parent)
        vol_label.setText("LOW PASS\nFILTER")
        vol_label.setGeometry(50, 275, 70, 28)
        vol_label.setStyleSheet("color:#502c22")
        vol_label.setAlignment(Qt.AlignCenter)
        vol_label.show()

        self.show()
        self.soundout = soundout

    def change_value(self, value):
        self.soundout.change_lowpass(-value)

    def get_value(self):
        return self.value()

    def load_value(self, value):
        self.setValue(value)
