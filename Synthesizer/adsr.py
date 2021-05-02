import time


class EnvADSR:

    def __init__(self, soundout):
        self.attack_time = 0.3
        self.decay_time = 0
        self.release_time = 0.3

        self.adsr_tail = False

        self.sustain_amp = 1
        self.rel_multiplier = 0
        self.adsr_amp = 0  # 0...1

        self.start_time = 0
        self.press_time = 0

        self.release_start_time = 0
        self.release_tail_time = 0

        self.soundout = soundout

    def get_adsr(self):
        if self.adsr_tail == False:
            self.press_time = time.time() - self.start_time

            if self.press_time <= self.attack_time: # Attack
                if self.attack_time == 0:
                    self.adsr_amp = 0
                else:
                    self.adsr_amp = self.press_time / self.attack_time
                self.rel_multiplier = self.adsr_amp
                return self.adsr_amp

            if  self.attack_time < self.press_time and self.press_time <= (self.attack_time + self.decay_time):  # Decay
                self.adsr_amp = (1-((self.press_time - self.attack_time) / self.decay_time)) \
                                * (self.soundout.get_amplitude() - self.sustain_amp*self.soundout.get_amplitude()) \
                                + self.sustain_amp*self.soundout.get_amplitude()

                self.rel_multiplier = self.adsr_amp / self.soundout.get_amplitude()
                if self.soundout.get_amplitude() == 0:
                    return 0
                else:
                    return self.adsr_amp / self.soundout.get_amplitude()

            if (self.attack_time + self.decay_time) < self.press_time:  # Sustain
                self.adsr_amp = self.sustain_amp
                self.rel_multiplier = self.adsr_amp
                return self.adsr_amp
        else:
            self.release_tail_time = time.time() - self.release_start_time

            if self.release_tail_time <= self.release_time and self.adsr_amp > 0.000001 and self.release_time != 0:
                self.adsr_amp = (1 - (self.release_tail_time / self.release_time)) * self.rel_multiplier
                return self.adsr_amp
            else:
                self.adsr_amp = 0
                self.soundout.set_key_played_false()
                return self.adsr_amp

    def set_start_time(self):
        self.start_time = time.time()
        self.adsr_tail = False

    def set_release_start_time(self):
        self.release_start_time = time.time()
        self.adsr_tail = True

    def one_key_at_once(self):
        self.adsr_tail = False

    def get_release_time(self):
        return self.release_time

    def change_adsr_knobs(self, value, type_is):
        if type_is == "ATTACK":
            self.attack_time = value / 100
        if type_is == "DECAY":
            self.decay_time = value / 100
        if type_is == "SUSTAIN":
            self.sustain_amp = value / 100
        if type_is == "RELEASE":
            self.release_time = value / 100
