from syra.config import load_config

config = load_config()
GPIO_ENABLED = config.get("hardware", {}).get("gpio_enabled", True)
MOTOR_DRIVER = config.get("hardware", {}).get("motor_driver", "mock")

def initialize(config=None):
    if not GPIO_ENABLED:
        print("[HARDWARE] GPIO interface disabled via config.")
        return

    try:
        print(f"[HARDWARE] Initializing motor driver: {MOTOR_DRIVER}")
        if MOTOR_DRIVER == "mock":
            print("[HARDWARE] Mock motor driver active.")
        elif MOTOR_DRIVER == "pwm_hat":
            print("[HARDWARE] PWM HAT driver not yet implemented.")
        elif MOTOR_DRIVER == "l298n":
            print("[HARDWARE] L298N driver not yet implemented.")
        else:
            print(f"[HARDWARE] Unknown motor driver: {MOTOR_DRIVER}")
        print("[INIT] Hardware system initialized.")
    except Exception as e:
        print(f"[HARDWARE ERROR] {e}")