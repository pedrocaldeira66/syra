# core/motion/eyelid_controller.py

from core.motion.servo_controller import ServoController
import os
import time

LEFT_UPPER_LID = int(os.getenv("LEFT_UPPER_LID_SERVO", 5))
RIGHT_UPPER_LID = int(os.getenv("RIGHT_UPPER_LID_SERVO", 6))

class EyelidController:
    def __init__(self):
        self.servo = ServoController()

    def blink(self, duration=0.1):
        self.close_eyelids()
        time.sleep(duration)
        self.open_eyelids()

    def close_eyelids(self):
        self.servo.set_angle(LEFT_UPPER_LID, 180)
        self.servo.set_angle(RIGHT_UPPER_LID, 180)

    def open_eyelids(self):
        self.servo.set_angle(LEFT_UPPER_LID, 60)
        self.servo.set_angle(RIGHT_UPPER_LID, 60)