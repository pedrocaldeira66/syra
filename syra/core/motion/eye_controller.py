# core/motion/eye_controller.py

from core.motion.servo_controller import ServoController
import os

# These can also be pulled from a hardware_config.json in the future
LEFT_EYE_H = int(os.getenv("LEFT_EYE_H_SERVO", 0))
LEFT_EYE_V = int(os.getenv("LEFT_EYE_V_SERVO", 1))
RIGHT_EYE_H = int(os.getenv("RIGHT_EYE_H_SERVO", 2))
RIGHT_EYE_V = int(os.getenv("RIGHT_EYE_V_SERVO", 3))

class EyeController:
    def __init__(self):
        self.servo = ServoController()

    def move_eyes(self, horiz_angle: int, vert_angle: int):
        horiz_angle = max(0, min(180, horiz_angle))
        vert_angle = max(0, min(180, vert_angle))

        self.servo.set_angle(LEFT_EYE_H, horiz_angle)
        self.servo.set_angle(RIGHT_EYE_H, horiz_angle)
        self.servo.set_angle(LEFT_EYE_V, vert_angle)
        self.servo.set_angle(RIGHT_EYE_V, vert_angle)

    def center_eyes(self):
        self.move_eyes(90, 90)