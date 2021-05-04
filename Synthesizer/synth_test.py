import unittest
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtTest import QTest
from soundout import *
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)

class TestParameters(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.main_w = MainWindow(app)
        #self.synth = SoundOut(self.main_w)
        self.synth = self.main_w.get_synth()
        self.main_w.show()
        QTest.qWaitForWindowExposed(self.main_w, 5)

    def test_volume(self):
        # Test that the knob cant go over 150 -> master amplitude cant go over 0.15
        self.main_w.get_master_knob().setValue(160)
        self.assertLessEqual(self.synth.get_amplitude(), 0.15)

        # if master amplitude raises over 0.15 it goes to zero
        self.synth.change_amplitude(151)
        self.assertEqual(self.synth.get_amplitude(), 0)

        # Test that the osc1 volume knob cant go over 150 -> osc amplitude amplifier cant go over 1
        self.main_w.get_osc_vol1().setValue(151)
        self.assertLessEqual(self.synth.get_osc().get_amplitude(), 1)

        # if osc1 amplitude multiplier raises over 1 it goes to zero
        self.synth.get_osc().change_amplitude(151)
        self.assertEqual(self.synth.get_osc().get_amplitude(), 0)

        # Test that the osc2 volume knob cant go over 150 -> osc amplitude amplifier cant go over 1
        self.main_w.get_osc_vol2().setValue(151)
        self.assertLessEqual(self.synth.get_osc2().get_amplitude(), 1)

        # if osc2 amplitude multiplier raises over 1 it goes to zero
        self.synth.get_osc2().change_amplitude(151)
        self.assertEqual(self.synth.get_osc2().get_amplitude(), 0)

    def tearDown(self):
        self.synth.close_stream()
        QCoreApplication.quit()
        self.main_w.close()
        app.exit()

if __name__ == "__main__":
    unittest.main()