
from state_machine import StateMachine
from face_display import FaceDisplay
from queue import Queue
import threading
import time

def main_loop():
    face_display = FaceDisplay()
    state_machine = StateMachine(face_display)

    # Simulierter Input
    def simulate_input():
        while True:
            input_queue.put("focus_detected")  # Fokussiert
            time.sleep(5)
            input_queue.put("no_focus")  # Abgelenkt
            time.sleep(5)
            
            
    # if kamera_erkennt_fokus():
    # input_queue.put("focus_detected")
    # else:
    # input_queue.put("no_focus")


    def process_input():
        while True:
            if not input_queue.empty():
                event = input_queue.get()
                state_machine.transition(event)
            time.sleep(0.1)

    input_queue = Queue()

    # Threads starten
    threading.Thread(target=simulate_input, daemon=True).start()
    threading.Thread(target=process_input, daemon=True).start()
    face_display.run()

if __name__ == "__main__":
    main_loop()