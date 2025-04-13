# core/motion/expressions.py

from core.motion.eye_controller import EyeController
from core.motion.mouth_controller import MouthController
from core.motion.eyelid_controller import EyelidController
import time

class Expressions:
    def __init__(self):
        self.eyes = EyeController()
        self.mouth = MouthController()
        self.lids = EyelidController()

    def neutral(self):
        self.eyes.center_eyes()
        self.lids.open_eyelids()
        self.mouth.close_mouth()

    def blink(self):
        self.lids.blink()

    def look_left(self):
        self.eyes.move_eyes(45, 90)

    def look_right(self):
        self.eyes.move_eyes(135, 90)

    def look_up(self):
        self.eyes.move_eyes(90, 45)

    def look_down(self):
        self.eyes.move_eyes(90, 135)

    def speak(self, phrase: str):
        pulse = [60, 120, 70, 110, 80, 100]
        for _ in range(len(phrase) // 3):
            self.mouth.speak_pulse(pulse)
            time.sleep(0.05)

    def surprised(self):
        self.eyes.center_eyes()
        self.lids.open_eyelids()
        self.mouth.open_mouth(150)

    def sad(self):
        self.eyes.move_eyes(90, 120)
        self.lids.close_eyelids()
        self.mouth.set_angle(60)