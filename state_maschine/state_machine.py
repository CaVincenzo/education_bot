import asyncio
import threading
import time
import sys
import os
import queue
# Füge das übergeordnete Verzeichnis zum Python-Pfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from face_display.face_display import FaceDisplay
from focus_recognition.focus_recognition_module import FocusRecognition
from LLM.lllm import LLMQuery

#TODO: für jede HandleMethode noch anpassen, wenn das dann zu dem Zustand wechslen ... 
class StateMachine:
    def __init__(self):
        # Initialzustand
        self.current_state = "Idle"
        self.face_display = FaceDisplay()
        self.focus_recognition = FocusRecognition()
        self.llm_query = LLMQuery() 
        
        # Warteschlange für GUI-Operationen
        self.gui_queue = queue.Queue()
        
        
       # Übergänge zwischen Zuständen
        self.transitions = {
            "Idle": {"focus_detected": "Fokussiert", "no_focus": "Abgelenkt"},
            "Fokussiert": {"no_focus": "Abgelenkt", "start_interaction": "Interaktion"},
            "Abgelenkt": {"focus_detected": "Fokussiert", "start_interaction": "Interaktion"},
            "Interaktion": {"end_interaction": "Idle"}
        }

        # Aktionen, die bei Zustandswechseln ausgeführt werden
        self.actions = {
            "Idle": self.handle_idle,
            "Fokussiert": self.handle_focus,
            "Abgelenkt": self.handle_distraction,
            "Interaktion": self.handle_interaction
        }    
        
    def handle_idle(self):
        print("State: Idle - Der Bot wartet auf eine Eingabe.")
        self.gui_queue.put(lambda: self.face_display.create_face(True))
         # Simulation eines Ereignisses
        time.sleep(10)  # Simuliert Arbeit
        self.transition("focus_detected")  # Wechsle zur Fokussierung

    def handle_focus(self):
        print("State: Fokussiert - Die Person arbeitet konzentriert.")
        self.gui_queue.put(lambda: self.face_display.create_face(True))  # Zeige ein lächelndes Gesicht
        time.sleep(2)
        
        self.transition("start_interaction")  # Wechsle zur Interaktion

    def handle_distraction(self):
        print("State: Abgelenkt - Die Person ist unkonzentriert.")
        self.gui_queue.put(lambda: self.face_display.create_face(False))  # Zeige ein trauriges Gesicht
        
        # Simulation: Nach einer kurzen Zeit wird Fokus erkannt
        time.sleep(2)
        self.transition("start_interaction")  # Wechsle zur Interaktion

    async def handle_interaction(self):
        print("State: Interaktion - Der Bot spricht mit der Person.")
        
        # Hier dann den Input aus dem Voice to Text zur Übergabe ans LLM für Prompt
        user_input = input("Bitte geben Sie Ihre Frage ein: ")
        prompt = f"BenutzerInput: {user_input}"
        
        # Query an LLM
        response = await self.llm_query.query_Mistral(prompt)
        
        # Print der Ausgabe oder an das entsprechende Text to Speech weiterleiten
        print("Antwort vom LLM:", response)
        
        self.transition("end_interaction")
        
    def simulate_input(self):
        while True:
            time.sleep(5)
            self.transition("focus_detected")
            time.sleep(5)
            self.transition("no_focus")
            time.sleep(5)
            self.transition("start_interaction")

    def handle_event(self, event):
        if event in self.transitions[self.current_state]:
            new_state = self.transitions[self.current_state][event]
            self.current_state = new_state
            if asyncio.iscoroutinefunction(self.actions[new_state]):
                asyncio.run(self.actions[new_state]())
            else:
                self.actions[new_state]() 

    def transition(self, event):
        if event in self.transitions[self.current_state]:
            new_state = self.transitions[self.current_state][event]
            print(f"Uebergang: {self.current_state} -> {new_state} durch Ereignis '{event}'")
            self.current_state = new_state
            
            # Aktion für neuen Zustand ausführen
            if asyncio.iscoroutinefunction(self.actions[self.current_state]):
                asyncio.run(self.actions[self.current_state]())
            else:
                self.actions[self.current_state]()
        else:
            print(f"Ereignis '{event}' ist im Zustand '{self.current_state}' nicht erlaubt.")


    def run(self):
        """
        Startet die State-Maschine und führt die Logik aus.
        """
        print("State-Maschine gestartet.")
        
        # Starte Threads für Input-Simulation und Verarbeitung
        threading.Thread(target=self.simulate_input, daemon=True).start()
        
        try:
            while True:
                # Aktion für aktuellen Zustand ausführen
                if asyncio.iscoroutinefunction(self.actions[self.current_state]):
                    asyncio.run(self.actions[self.current_state]())
                else:
                    self.actions[self.current_state]()
                
                # Verarbeite GUI-Operationen
                while not self.gui_queue.empty():
                    gui_operation = self.gui_queue.get()
                    gui_operation()
                
                time.sleep(1)  # Kurze Verzögerung zwischen den Zustandsprüfungen
        except KeyboardInterrupt:
            print("State-Maschine beendet.")
            

def main():
    state_machine = StateMachine()
    state_machine.run()

if __name__ == "__main__":
    main()

test