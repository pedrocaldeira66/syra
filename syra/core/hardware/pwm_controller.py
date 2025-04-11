import os
from dotenv import load_dotenv

load_dotenv()

I2C_ADDR = int(os.getenv("PCA9685_ADDR", "0x40"), 16)
PWM_FREQ = int(os.getenv("PWM_FREQ", "50"))  # Hz — typical for ESCs

class PWMController:
    def __init__(self):
        import board
        import busio
        from adafruit_pca9685 import PCA9685

        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c, address=I2C_ADDR)
        self.pca.frequency = PWM_FREQ

        # Assume channels 0–3 for motors
        self.motor_channels = [self.pca.channels[i] for i in range(4)]

    def set_motor_speed(self, index, duty):
        """Set motor PWM duty cycle. Value range: 0.0 to 1.0"""
        if 0 <= index < len(self.motor_channels):
            pwm_val = int(duty * 0xFFFF)
            self.motor_channels[index].duty_cycle = pwm_val
        else:
            raise IndexError("Invalid motor index")

    def shutdown(self):
        for channel in self.motor_channels:
            channel.duty_cycle = 0
        self.pca.deinit()
