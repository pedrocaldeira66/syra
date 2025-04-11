import serial
import pynmea2
import time

class GPSInterface:
    def __init__(self, port="/dev/serial0", baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)  # Wait for GPS module to stabilize

    def read_sentence(self):
        try:
            line = self.ser.readline().decode("ascii", errors="replace")
            if line.startswith("$"):
                return pynmea2.parse(line)
        except (pynmea2.ParseError, UnicodeDecodeError):
            return None

    def get_location(self):
        while True:
            msg = self.read_sentence()
            if msg and isinstance(msg, pynmea2.types.talker.GGA):
                return {
                    "lat": msg.latitude,
                    "lon": msg.longitude,
                    "alt": msg.altitude,
                    "timestamp": msg.timestamp
                }
