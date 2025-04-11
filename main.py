from syra.boot import boot_sequence
from syra.core.speech import get_stt, get_tts
from syra.core.vision import OpenCVCamera
from core.reasoning.reasoning import ReasoningEngine
from syra.core.memory import MemoryStore
from syra.core.hardware import HardwareInterface
from syra.utils.safe_init import safe_init
import time

def main():
    config = boot_sequence()

    print("[AGENT] Initializing SYRA core components...")
    stt = safe_init(get_stt, name="STT Engine")
    tts = safe_init(get_tts, name="TTS Engine")
    cam = safe_init(OpenCVCamera, name="Vision Camera")
    memory = safe_init(MemoryStore, name="Memory Store")
    brain = safe_init(ReasoningEngine, name="Reasoning Engine")
    hardware = safe_init(HardwareInterface, name="Hardware Interface")

    print("[AGENT] SYRA is live. Entering main loop.")

    try:
        while True:
            # Perception Phase
            perception = {}
            if stt:
                spoken = safe_init(stt.listen, name="STT Listen")
                if spoken:
                    perception["speech"] = spoken
            if cam:
                frame = safe_init(cam.get_frame, name="Camera Frame")
                if frame is not None:
                    perception["vision"] = "[frame captured]"  # Placeholder for processing

            memory.update(perception)

            # Reasoning & Action Phase
            plan = brain.generate_plan(perception, memory)
            action = brain.select_action(plan)

            # Action Execution Phase
            if hardware:
                safe_init(lambda: hardware.execute(action), name="Hardware Execute")
            if tts:
                safe_init(lambda: tts.speak(action), name="TTS Speak")

            memory.log_interaction(perception, plan, action)

            if hardware:
                safe_init(hardware.monitor_system, name="System Monitor")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[AGENT] Shutting down...")
        if cam:
            cam.release()
        if memory:
            memory.save()

if __name__ == "__main__":
    main()
