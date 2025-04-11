import os
from dotenv import load_dotenv

load_dotenv()

GPIO_ENABLED = os.getenv("GPIO_ENABLED", "false").lower() == "true"
MOTOR_DRIVER = os.getenv("MOTOR_DRIVER", "mock").lower()

# Import hardware modules
from syra.core.hardware.pwm_controller import PWMController
from syra.core.hardware.imu_interface import IMUInterface
from syra.core.hardware.adc_interface import ADCInterface
from syra.core.hardware.gps_interface import GPSInterface

class HardwareInterface:
    def __init__(self):
        self.motor = None
        self.imu = None
        self.adc = None
        self.gps = None

        if GPIO_ENABLED:
            if MOTOR_DRIVER == "pwm_hat":
                try:
                    self.motor = PWMController()
                    print("[HARDWARE] PWMController initialized (PCA9685)")
                except Exception as e:
                    print(f"[ERROR] Failed to init PWMController: {e}")
            else:
                print(f"[HARDWARE] MOTOR_DRIVER '{MOTOR_DRIVER}' is not implemented yet.")

            try:
                self.imu = IMUInterface()
                print("[HARDWARE] MPU6050 IMU initialized")
            except Exception as e:
                print(f"[ERROR] Failed to init IMU: {e}")

            try:
                self.adc = ADCInterface()
                print("[HARDWARE] ADS1115 ADC initialized")
            except Exception as e:
                print(f"[ERROR] Failed to init ADC: {e}")

            try:
                self.gps = GPSInterface()
                print("[HARDWARE] GPS module initialized")
            except Exception as e:
                print(f"[ERROR] Failed to init GPS: {e}")
        else:
            print("[HARDWARE] GPIO is disabled in .env")

    def execute(self, action):
        print(f"[HARDWARE] Executing action: {action}")
        # In future: decode action → PWM or movement

    def monitor_system(self):
        print("[HARDWARE] Monitoring system status...")
        # In future: read voltages, temp, etc.
