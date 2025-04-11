import logging
from syra.config import config
from syra.utils.safe_init import safe_import

logger = logging.getLogger(__name__)

USE_MOCK = config.get("USE_MOCK", "false").lower() == "true"
PWM_DRIVER = config.get("PWM_DRIVER", "mock")

if USE_MOCK or PWM_DRIVER == "mock":
    class PWMController:
        def __init__(self):
            logger.debug("[PWM] Using mock PWM controller")

        def set_pwm(self, channel, duty_cycle):
            logger.info(f"[PWM] [MOCK] Setting PWM on channel {channel} to {duty_cycle}%")

else:
    Adafruit_PCA9685 = safe_import("Adafruit_PCA9685")

    class PWMController:
        def __init__(self, freq=50):
            self.pwm = Adafruit_PCA9685.PCA9685()
            self.pwm.set_pwm_freq(freq)
            logger.info(f"[PWM] PCA9685 initialized at {freq}Hz")

        def set_pwm(self, channel, duty_cycle):
            pulse = int(duty_cycle / 100.0 * 4095)
            self.pwm.set_pwm(channel, 0, pulse)
            logger.debug(f"[PWM] Set channel {channel} to {pulse}/4095")

def initialize(config):
    logger.info("[INIT] PWM controller initialized.")