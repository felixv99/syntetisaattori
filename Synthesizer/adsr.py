#from oscillator import Oscillator
import time
class EnvADSR:

    def __init__(self,soundout):
        self.attack_time = 0.3
        #self.decay_time = 0
        #self.release_time = 0


        #self.start_amp = 0
        #self.sustain_amp = 0
        self.adsr_amp = 0  # 0...1
        self.start_time = 0
        self.press_time = 0

        self.soundout = soundout
    def get_adsr(self):
        if self.soundout.is_key_played():
            self.press_time = time.time() - self.start_time
            if self.press_time <= self.attack_time:
                self.adsr_amp = self.press_time / self.attack_time
                #print("TEST")
                return self.adsr_amp
            else:
                #print("ATTACK")
                return 1
        else:
                return 1

    def set_start_time(self):
        self.start_time = time.time()

    def change_attack_time(self, value):
        self.attack_time = value / 100
