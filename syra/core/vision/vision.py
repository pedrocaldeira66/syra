from syra.config import load_config
import cv2

config = load_config()

VISION_ENABLED = config.get("vision", {}).get("enabled", True)
CAMERA_SOURCE = config.get("vision", {}).get("camera_source", "usb")
FRAME_WIDTH = int(config.get("vision", {}).get("frame_width", 640))
FRAME_HEIGHT = int(config.get("vision", {}).get("frame_height", 480))

camera = None

def initialize(config=None):
    if not VISION_ENABLED:
        print("[VISION] Vision system is disabled via config.")
        return

    try:
        global camera
        if CAMERA_SOURCE == "usb":
            camera = cv2.VideoCapture(0)
        elif CAMERA_SOURCE == "mock":
            print("[VISION] Using mock camera.")
            return
        else:
            print(f"[VISION] Unsupported camera source: {CAMERA_SOURCE}")
            return

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        print("[INIT] Vision system initialized.")
    except Exception as e:
        print(f"[VISION ERROR] Initialization failed: {e}")

def capture_frame():
    if not camera:
        print("[VISION] Camera not initialized.")
        return None

    ret, frame = camera.read()
    if not ret:
        print("[VISION] Failed to read frame.")
        return None
    return frame