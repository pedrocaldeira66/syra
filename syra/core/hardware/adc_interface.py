import os
from dotenv import load_dotenv

load_dotenv()

I2C_ADDR = int(os.getenv("ADS1115_ADDR", "0x48"), 16)
ADC_GAIN = int(os.getenv("ADC_GAIN", "1"))

class ADCInterface:
    def __init__(self):
        import board
        import busio
        from adafruit_ads1x15.ads1115 import ADS1115
        from adafruit_ads1x15.analog_in import AnalogIn

        i2c = busio.I2C(board.SCL, board.SDA)
        self.ads = ADS1115(i2c, address=I2C_ADDR)
        self.ads.gain = ADC_GAIN

        # Create channels
        self.channels = [AnalogIn(self.ads, getattr(ADS1115, f"P{i}")) for i in range(4)]

    def read_all(self):
        return [ch.voltage for ch in self.channels]

    def read_channel(self, index):
        if 0 <= index < 4:
            return self.channels[index].voltage
        raise IndexError("ADC channel index out of range")
