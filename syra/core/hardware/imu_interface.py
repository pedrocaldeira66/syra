import time
import smbus2
import math

class IMUInterface:
    def __init__(self, bus=1, address=0x68):
        self.address = address
        self.bus = smbus2.SMBus(bus)

        # Wake up the MPU6050 (clear sleep bit)
        self.bus.write_byte_data(self.address, 0x6B, 0x00)
        time.sleep(0.1)

    def read_raw_data(self, reg):
        high = self.bus.read_byte_data(self.address, reg)
        low = self.bus.read_byte_data(self.address, reg + 1)
        value = (high << 8) | low
        return value - 65536 if value > 32767 else value

    def read_accel_gyro(self):
        accel = {
            "x": self.read_raw_data(0x3B) / 16384.0,
            "y": self.read_raw_data(0x3D) / 16384.0,
            "z": self.read_raw_data(0x3F) / 16384.0,
        }
        gyro = {
            "x": self.read_raw_data(0x43) / 131.0,
            "y": self.read_raw_data(0x45) / 131.0,
            "z": self.read_raw_data(0x47) / 131.0,
        }
        return {"accel": accel, "gyro": gyro}
