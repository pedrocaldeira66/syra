# syra/core/hardware/imu_interface.py

import time
import logging
from syra.config import config
from syra.utils.safe_init import safe_import

logger = logging.getLogger(__name__)

USE_MOCK = config.get("USE_MOCK", "false").lower() == "true"
IMU_DRIVER = config.get("IMU_DRIVER", "mock")

if USE_MOCK or IMU_DRIVER == "mock":
    class IMU:
        def __init__(self):
            logger.debug("[IMU] Using mock IMU interface")

        def read(self):
            logger.debug("[IMU] Returning mock IMU data")
            return {
                "accel_x": 0.01,
                "accel_y": 0.01,
                "accel_z": 0.98,
                "gyro_x": 0.02,
                "gyro_y": 0.01,
                "gyro_z": -0.01,
            }

else:
    smbus = safe_import("smbus")

    class IMU:
        def __init__(self):
            self.bus = smbus.SMBus(1)
            self.address = 0x68
            self.bus.write_byte_data(self.address, 0x6B, 0)  # Wake up MPU6050
            logger.info("[IMU] MPU6050 initialized at 0x68")

        def _read_word(self, reg):
            high = self.bus.read_byte_data(self.address, reg)
            low = self.bus.read_byte_data(self.address, reg + 1)
            value = (high << 8) + low
            return value - 65536 if value >= 0x8000 else value

        def read(self):
            try:
                return {
                    "accel_x": self._read_word(0x3B) / 16384.0,
                    "accel_y": self._read_word(0x3D) / 16384.0,
                    "accel_z": self._read_word(0x3F) / 16384.0,
                    "gyro_x": self._read_word(0x43) / 131.0,
                    "gyro_y": self._read_word(0x45) / 131.0,
                    "gyro_z": self._read_word(0x47) / 131.0,
                }
            except Exception as e:
                logger.error(f"[IMU] Read error: {e}")
                return None

def initialize(config):
    logger.info("[INIT] IMU interface initialized.")