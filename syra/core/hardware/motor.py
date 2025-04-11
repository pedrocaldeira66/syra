from syra.config import load_config

config = load_config()
MOTOR_DRIVER = config.get("hardware", {}).get("motor_driver", "mock")

class Motor:
    def __init__(self, name="motor", driver=MOTOR_DRIVER):
        self.name = name
        self.driver = driver

        if self.driver == "mock":
            print(f"[MOTOR:{self.name}] Initialized in mock mode.")
        elif self.driver == "pwm_hat":
            print(f"[MOTOR:{self.name}] PWM HAT control not yet implemented.")
        elif self.driver == "l298n":
            print(f"[MOTOR:{self.name}] L298N motor control not yet implemented.")
        else:
            print(f"[MOTOR:{self.name}] Unknown driver: {self.driver}")

    def move(self, direction="forward", speed=100):
        if self.driver == "mock":
            print(f"[MOTOR:{self.name}] Simulated move {direction} at speed {speed}")
        else:
            print(f"[MOTOR:{self.name}] Real move not implemented yet")