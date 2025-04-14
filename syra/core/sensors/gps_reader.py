# core/sensors/gps_reader.py

import os
import serial
from dotenv import load_dotenv

load_dotenv()

GPS_PORT = os.getenv("GPS_PORT", "/dev/serial0")
GPS_BAUDRATE = int(os.getenv("GPS_BAUDRATE", 9600))

def parse_nmea_sentence(nmea):
    if nmea.startswith('$GPGGA'):
        parts = nmea.split(',')
        if parts[2] and parts[4]:
            lat = convert_to_decimal(parts[2], parts[3])
            lon = convert_to_decimal(parts[4], parts[5])
            return lat, lon
    return None, None

def convert_to_decimal(coord, direction):
    deg = int(coord[:2]) if direction in ['N', 'S'] else int(coord[:3])
    minutes = float(coord[len(str(deg)):])
    decimal = deg + (minutes / 60)
    if direction in ['S', 'W']:
        decimal *= -1
    return round(decimal, 6)

def read_gps():
    try:
        with serial.Serial(GPS_PORT, GPS_BAUDRATE, timeout=1) as ser:
            print("[GPS] Listening on", GPS_PORT)
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith('$GPGGA'):
                    lat, lon = parse_nmea_sentence(line)
                    if lat and lon:
                        print(f"[GPS] Location: {lat}, {lon}")
    except serial.SerialException as e:
        print(f"[GPS] Serial error: {e}")
    except KeyboardInterrupt:
        print("[GPS] Stopped by user.")

if __name__ == "__main__":
    read_gps()