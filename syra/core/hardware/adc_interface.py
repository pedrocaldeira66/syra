# syra/core/hardware/adc_interface.py

import os
import logging

from syra.config import config
from syra.utils.safe_init import safe_import

logger = logging.getLogger(__name__)

# Determine whether to use mock or real ADC
USE_MOCK = config.get("USE_MOCK", "false").lower() == "true"
ADC_DRIVER = config.get("ADC_DRIVER", "mock")

if USE_MOCK or ADC_DRIVER == "mock":
    class ADC:
        def __init__(self):
            logger.debug("[ADC] Using mock ADC interface")

        def read_channel(self, channel):
            logger.debug(f"[ADC] Reading mock channel {channel}")
            return 1234  # Simulated value

else:
    # Attempt to import the real ADC driver (e.g., Adafruit_ADS1x15)
    ADS1115 = safe_import("adafruit_ads1x15.ads1115")
    AnalogIn = safe_import("adafruit_ads1x15.analog_in")
    import board
    import busio

    class ADC:
        def __init__(self):
            logger.info("[ADC] Initializing real ADS1115")
            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.adc = ADS1115.ADS1115(self.i2c)
            logger.debug("[ADC] ADS1115 initialized")

        def read_channel(self, channel):
            logger.debug(f"[ADC] Reading from channel {channel}")
            chan = AnalogIn.AnalogIn(self.adc, getattr(AnalogIn, f"P{channel}"))
            return chan.value

def initialize(config):
    logger.info("[INIT] ADC interface initialized.")