# core/motion/mouth_controller.py

from core.motion.servo_controller import ServoController
import os

MOUTH_SERVO = int(os.getenv("MOUTH_SERVO", 4))

class MouthController:
    def __init__(self):
        self.servo = ServoController()

    def open_mouth(self, angle=120):
        self.servo.set_angle(MOUTH_SERVO, angle)

    def close_mouth(self):
        self.servo.set_angle(MOUTH_SERVO, 60)

    def speak_pulse(self, pattern: list):
        for angle in pattern:
            self.servo.set_angle(MOUTH_SERVO, angle)