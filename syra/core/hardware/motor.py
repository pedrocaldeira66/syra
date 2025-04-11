# syra/core/hardware/motor.py

import logging
from syra.config import config

logger = logging.getLogger(__name__)

USE_MOCK = config.get("USE_MOCK", "false").lower() == "true"
MOTOR_DRIVER = config.get("MOTOR_DRIVER", "mock")

class Motor:
    def __init__(self, name="motor", driver=None):
        self.name = name
        self.driver = driver or MOTOR_DRIVER

        if USE_MOCK or self.driver == "mock":
            self.mode = "mock"
            logger.debug(f"[MOTOR:{self.name}] Mock motor initialized.")
        elif self.driver == "pwm_hat":
            self.mode = "pwm_hat"
            logger.debug(f"[MOTOR:{self.name}] PWM HAT motor ready.")
        elif self.driver == "l298n":
            self.mode = "l298n"
            logger.debug(f"[MOTOR:{self.name}] L298N motor configured.")
        else:
            logger.warning(f"[MOTOR:{self.name}] Unknown driver '{self.driver}'. Defaulting to mock.")
            self.mode = "mock"

    def move(self, direction="forward", speed=100):
        if self.mode == "mock":
            logger.info(f"[MOTOR:{self.name}] Simulated move {direction} at speed {speed}")
        elif self.mode == "pwm_hat":
            logger.info(f"[MOTOR:{self.name}] (PWM HAT) Move {direction} @ {speed}% - [not implemented]")
        elif self.mode == "l298n":
            logger.info(f"[MOTOR:{self.name}] (L298N) Move {direction} @ {speed}% - [not implemented]")
        else:
            logger.error(f"[MOTOR:{self.name}] Cannot move: unknown driver mode")

def initialize(config=None):
    logger.info("[INIT] Motor driver initialized.")