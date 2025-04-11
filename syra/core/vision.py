import os
import cv2
from dotenv import load_dotenv

load_dotenv()

CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "usb")
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", "640"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", "480"))

class OpenCVCamera:
    def __init__(self):
        # Map source type to actual device index or path
        if CAMERA_SOURCE == "usb":
            self.cap = cv2.VideoCapture(0)
        elif CAMERA_SOURCE == "pi":
            self.cap = cv2.VideoCapture(0)  # Placeholder, Pi camera support depends on build
        elif CAMERA_SOURCE.startswith("/dev/"):
            self.cap = cv2.VideoCapture(CAMERA_SOURCE)
        else:
            raise ValueError(f"[ERROR] Unsupported CAMERA_SOURCE: {CAMERA_SOURCE}")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        if not self.cap.isOpened():
            raise RuntimeError(f"[ERROR] Could not open camera: {CAMERA_SOURCE}")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("[ERROR] Failed to capture frame from camera.")
        return frame

    def release(self):
        if self.cap:
            self.cap.release()

def initialize(config):
    print(f"[INIT] Vision system initialized with source: {CAMERA_SOURCE}, resolution: {FRAME_WIDTH}x{FRAME_HEIGHT}")
