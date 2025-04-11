# syra/core/hardware/gps_interface.py

import logging
import time

from syra.config import config
from syra.utils.safe_init import safe_import

logger = logging.getLogger(__name__)

USE_MOCK = config.get("USE_MOCK", "false").lower() == "true"
GPS_DRIVER = config.get("GPS_DRIVER", "mock")

if USE_MOCK or GPS_DRIVER == "mock":
    class GPS:
        def __init__(self):
            logger.debug("[GPS] Using mock GPS module")

        def get_location(self):
            logger.debug("[GPS] Returning mock GPS data")
            return {"lat": 38.8, "lon": -9.1, "alt": 12.5}

else:
    serial = safe_import("serial")
    pynmea2 = safe_import("pynmea2")

    class GPS:
        def __init__(self):
            logger.info("[GPS] Initializing real GPS module")
            port = config.get("GPS_SERIAL_PORT", "/dev/ttyAMA0")
            baudrate = int(config.get("GPS_BAUDRATE", "9600"))
            self.ser = serial.Serial(port, baudrate, timeout=1)
            logger.debug(f"[GPS] Serial port {port} opened at {baudrate} bps")

        def get_location(self):
            try:
                while True:
                    line = self.ser.readline().decode("utf-8", errors="ignore")
                    if line.startswith("$GPGGA"):
                        msg = pynmea2.parse(line)
                        return {
                            "lat": msg.latitude,
                            "lon": msg.longitude,
                            "alt": msg.altitude,
                        }
            except Exception as e:
                logger.error(f"[GPS] Error parsing GPS data: {e}")
                return None

def initialize(config):
    logger.info("[INIT] GPS interface initialized.")