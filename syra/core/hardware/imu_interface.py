import time
from syra.config import load_config

try:
    import smbus
except ImportError:
    smbus = None
    print("[IMU] smbus module not available — running in mock mode.")

config = load_config()
USE_MOCK = config.get("use_mock", False)

class IMU:
    def __init__(self):
        if USE_MOCK or smbus is None:
            self.mock = True
            print("[IMU] Running in mock mode.")
        else:
            self.mock = False
            self.bus = smbus.SMBus(1)
            self.address = 0x68
            self.bus.write_byte_data(self.address, 0x6B, 0)  # Wake up MPU-6050
            print("[IMU] Initialized MPU-6050 at I2C address 0x68.")

    def read(self):
        if self.mock:
            return {
                "accel_x": 0,
                "accel_y": 0,
                "accel_z": 1,
                "gyro_x": 0,
                "gyro_y": 0,
                "gyro_z": 0,
            }

        def read_word(reg):
            high = self.bus.read_byte_data(self.address, reg)
            low = self.bus.read_byte_data(self.address, reg + 1)
            val = (high << 8) + low
            return val - 65536 if val >= 0x8000 else val

        return {
            "accel_x": read_word(0x3B) / 16384.0,
            "accel_y": read_word(0x3D) / 16384.0,
            "accel_z": read_word(0x3F) / 16384.0,
            "gyro_x": read_word(0x43) / 131.0,
            "gyro_y": read_word(0x45) / 131.0,
            "gyro_z": read_word(0x47) / 131.0,
        }