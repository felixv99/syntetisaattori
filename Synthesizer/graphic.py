from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QDial)
from PyQt5.QtCore import Qt

class WaveSlider(QSlider):

    def __init__(self, parent, synth):
        super(WaveSlider, self).__init__(parent)
       # wave_slider = QSlider(Qt.Horizontal, self)
        #wave_slider.setGeometry(30, 40, 200, 30)
        #wave_slider.valueChanged[int].connect(self.changeValue)
        self.setGeometry(210, 70, 40, 120)
        self.setMinimum(1)
        self.setMaximum(3)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setSliderPosition(3)
        self.valueChanged.connect(self.change_value)
        sin_label = QLabel(parent)
        sin_label.setText("SIN")
        sin_label.setGeometry(245,25, 100, 100)
        sin_label.show()
        square_label = QLabel(parent)
        square_label.setText("SQUARE")
        square_label.setGeometry(245, 80, 100, 100)
        square_label.show()
        saw_label = QLabel(parent)
        saw_label.setText("SAW")
        saw_label.setGeometry(245, 135, 100, 100)
        saw_label.show()
        wave_label = QLabel(parent)
        wave_label.setText("WAVE")
        wave_label.setGeometry(245, 0, 100, 100)
        wave_label.show()
        self.show()
        self.synth = synth

        sin_label = QLabel(self)
        sin_label.setText("SIN")

    def change_value(self, value):
        self.synth.get_osc().change_wave(value)
        print(value)


class OctaveSlider(QSlider):

    def __init__(self, parent, osc):
        super(OctaveSlider, self).__init__(parent)
        self.setGeometry(90, 70, 40, 120)
        self.setMinimum(-1)
        self.setMaximum(3)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)
        self.setSliderPosition(1)
        self.valueChanged.connect(self.change_value)
        oct_label = QLabel(parent)
        oct_label.setText("OCTAVE")
        oct_label.setGeometry(90, 0, 100, 100)
        oct_label.show()
        self.show()
        self.osc = osc

    def change_value(self, value):
        self.osc.change_octave(value)
        #print(value)


class VolumeKnob(QDial):

    def __init__(self, parent, osc):
        super(VolumeKnob, self).__init__(parent)
        self.setGeometry(380, 70, 120, 120)
        self.setMinimum(0)
        self.setMaximum(150)
        #self.setTickPosition(QSlider.TicksBelow)
        #self.setTickInterval(1)
        self.setValue(30)
        self.valueChanged.connect(self.change_value)
        vol_label = QLabel(parent)
        vol_label.setText("VOLUME")
        vol_label.setGeometry(410, 0, 100, 100)
        vol_label.show()
        self.show()
        self.osc = osc

    def change_value(self, value):
        self.osc.change_amplitude(value)
        print(value)


class ADSRKnob(QDial):

    def __init__(self, parent, osc):
        super(ADSRKnob, self).__init__(parent)
        self.setGeometry(570, 70, 80, 80)
        self.setMinimum(0)
        self.setMaximum(500)
        #self.setTickPosition(QSlider.TicksBelow)
        #self.setTickInterval(1)
        self.setValue(60)
        self.valueChanged.connect(self.change_value)
        vol_label = QLabel(parent)
        vol_label.setText("ATTACK")
        vol_label.setGeometry(585, 0, 100, 100)
        vol_label.show()
        self.show()
        self.adsr = osc.get_adsr()

    def change_value(self, value):
        self.adsr.change_attack_time(value)
        print(value)


"""
class ADSRKnob2(QDial):
    ATTACK = 1
    DECAY = 2
    SUSTAIN = 3
    RELEASE = 4
    def __init__(self, parent, osc):
        super(ADSRKnob2, self).__init__(parent)
        self.setGeometry(670, 70, 80, 80)
        self.setMinimum(0)
        self.setMaximum(500)
        #self.setTickPosition(QSlider.TicksBelow)
        #self.setTickInterval(1)
        self.setValue(60)
        self.valueChanged.connect(self.change_value)
        vol_label = QLabel(parent)
        vol_label.setText("RELEASE")
        vol_label.setGeometry(685, 0, 100, 100)
        vol_label.show()
        self.show()
        self.adsr = osc.get_adsr()

    def change_value(self, value):
        self.adsr.change_attack_time(value)
        print(value)
"""