# core/motion/servo_controller.py

import os
from dotenv import load_dotenv
from core.utils.safe_import import safe_import

load_dotenv()

PWM_FREQ = 50  # Standard for servos
I2C_ADDRESS = int(os.getenv("PCA9685_ADDRESS", "0x40"), 16)

Adafruit_PCA9685 = safe_import("Adafruit_PCA9685")

class ServoController:
    def __init__(self, address=I2C_ADDRESS, freq=PWM_FREQ):
        if Adafruit_PCA9685 is None:
            raise ImportError("Adafruit_PCA9685 not available. Check I2C and dependency.")

        self.pwm = Adafruit_PCA9685.PCA9685(address)
        self.pwm.set_pwm_freq(freq)
        self.min_pulse = 150  # Adjust if needed
        self.max_pulse = 600  # Adjust if needed

    def angle_to_pwm(self, angle):
        angle = max(0, min(180, angle))
        return int(self.min_pulse + (angle / 180) * (self.max_pulse - self.min_pulse))

    def set_angle(self, channel, angle):
        pwm_val = self.angle_to_pwm(angle)
        self.pwm.set_pwm(channel, 0, pwm_val)