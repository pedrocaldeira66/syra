from syra.utils.safe_init import safe_init

import time

def main_loop(sensors, memory, reasoning, hardware, speech, max_cycles=5):
    cycle = 0
    while True:
        if max_cycles and cycle >= max_cycles:
            print("[LOOP] Max cycles reached, exiting.")
            break

        perception = sensors.get_input()
        memory.update(perception)

        plan = reasoning.generate_plan(perception, memory)
        action = reasoning.select_action(plan)

        hardware.execute(action)
        speech.respond(action)
        memory.log_interaction(perception, plan, action)

        hardware.monitor_system()
        cycle += 1
        time.sleep(1)  # Add delay to slow it down
