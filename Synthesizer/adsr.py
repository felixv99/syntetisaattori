#from oscillator import Oscillator
import time
class EnvADSR:

    def __init__(self,soundout):
        self.attack_time = 0.3
        self.decay_time = 0
        self.release_time = 0.3

        self.adsr_tail = False

        #self.start_amp = 0
        self.sustain_amp = 1
        self.adsr_amp = 0  # 0...1

        self.start_time = 0
        self.press_time = 0

        self.release_start_time = 0
        self.release_tail_time = 0
        self.soundout = soundout
    def get_adsr(self):
        #if self.soundout.is_key_played() == True:
        if self.adsr_tail == False:
            #print(self.soundout.is_key_played())
            self.press_time = time.time() - self.start_time


            if self.press_time <= self.attack_time: # Attack
                self.adsr_amp = self.press_time / self.attack_time
                #print(self.press_time)
                return self.adsr_amp

            if self.press_time > self.attack_time and self.press_time <= (self.attack_time + self.decay_time):  # Decay
                self.adsr_amp = (1-((self.press_time - self.attack_time) / self.decay_time))*(self.soundout.get_osc().get_amplitude() - self.sustain_amp*self.soundout.get_osc().get_amplitude())+self.sustain_amp*self.soundout.get_osc().get_amplitude()
                print(self.adsr_amp)
                return self.adsr_amp / self.soundout.get_osc().get_amplitude()
                # self.adsr_amp = ((self.press_time - self.attack_time) / self.decay_time) + (self.sustain_amp - self.soundout.get_osc().get_amplitude())
                # return (self.adsr_amp + self.soundout.get_osc().get_amplitude())/self.soundout.get_osc().get_amplitude()

            if self.press_time > self.attack_time + self.decay_time:  # Sustain
                #self.adsr_amp = self.sustain_amp / self.soundout.get_osc().get_amplitude()
                self.adsr_amp = self.sustain_amp
                #print("sustain?")
                return self.adsr_amp
            '''
            else:
                return 0
            '''
        else:
            #print("release1")
            self.release_tail_time = time.time() - self.release_start_time
            #print("TEST2")
            if self.release_tail_time <= self.release_time and self.adsr_amp > 0.0001:
                self.adsr_amp = (1 - (self.release_tail_time / self.release_time))* self.sustain_amp
                #print("release2")
                return self.adsr_amp
            else:
                self.adsr_amp = 0
                #print(self.release_start_time)
                self.soundout.set_key_played_false()
                return self.adsr_amp

    def set_start_time(self):
        self.start_time = time.time()
        self.adsr_tail = False

    def get_release_time(self):
        return self.release_time

    def set_release_start_time(self):
        self.release_start_time = time.time()
        print("OG START TIME", self.release_start_time)
        self.adsr_tail = True
    '''
    def change_attack_time(self, value):
        self.attack_time = value / 100

    def change_release_time(self, value):
        self.release_time = value / 100
    '''
    def change_adsr_knobs(self, value, type_is):
        if type_is == "ATTACK":
            self.attack_time = value / 100
        if type_is == "DECAY":
            self.decay_time = value / 100
        if type_is == "SUSTAIN":
            #self.sustain_amp = value / 1000
            self.sustain_amp = value / 100
        if type_is == "RELEASE":
            self.release_time = value / 100

    '''
    def change_sustain_with_amplitude(self, value):
        self.sustain_amp = self.sustain_amp*value   # SUSTAIN EI TOIMI KUNNOLLA VOLYYMIN VAIHDON JÄLKEEN!!
    '''