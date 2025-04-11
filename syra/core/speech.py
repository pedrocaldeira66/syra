import os
from syra.utils.safe_init import safe_import
from dotenv import load_dotenv

load_dotenv()

# Load environment configuration
SPEECH_MODE = os.getenv("SPEECH_MODE", "offline")
STT_ENGINE = os.getenv("STT_ENGINE", "vosk").lower()
TTS_ENGINE = os.getenv("TTS_ENGINE", "coqui").lower()

# ---------- STT Engines ----------

class VoskSTT:
    def __init__(self):
        from vosk import Model, KaldiRecognizer
        import sounddevice as sd
        import queue
        import json

        self.q = queue.Queue()
        model_path = os.getenv("VOSK_MODEL_PATH", "models/vosk")
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

        def callback(indata, frames, time, status):
            if status:
                print(f"[VOSK] Audio status: {status}")
            self.q.put(bytes(indata))

        self.stream = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                        channels=1, callback=callback)
        self.stream.start()

    def listen(self):
        import json
        while True:
            data = self.q.get()
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                return result.get("text", "")

# ---------- TTS Engines ----------

class CoquiTTS:
    def __init__(self):
        from TTS.api import TTS
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

    def speak(self, text):
        self.tts.tts_to_file(text=text, file_path="output.wav")

        import simpleaudio as sa
        wave_obj = sa.WaveObject.from_wave_file("output.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()

# ---------- Module Init + Interface ----------

def initialize(config):
    print(f"[INIT] Speech system initialized with STT={STT_ENGINE}, TTS={TTS_ENGINE}")

def get_stt():
    if STT_ENGINE == "vosk":
        return VoskSTT()
    raise ValueError(f"[ERROR] Unsupported STT engine: {STT_ENGINE}")

def get_tts():
    if TTS_ENGINE == "coqui":
        return CoquiTTS()
    raise ValueError(f"[ERROR] Unsupported TTS engine: {TTS_ENGINE}")
