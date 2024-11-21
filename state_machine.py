
class StateMachine:
    def __init__(self, face_display):
        # Initialzustand
        self.current_state = "Idle"
        self.face_display = face_display

        # Übergänge zwischen Zuständen
        self.transitions = {
            "Idle": {
                "focus_detected": "Fokussiert",
                "no_focus": "Abgelenkt"
            },
            "Fokussiert": {
                "no_focus": "Abgelenkt",
                "start_interaction": "Interaktion"
            },
            "Abgelenkt": {
                "focus_detected": "Fokussiert",
                "start_interaction": "Interaktion"
            },
            "Interaktion": {
                "end_interaction": "Idle"
            }
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

    def handle_focus(self):
        print("State: Fokussiert - Die Person arbeitet konzentriert.")

    def handle_distraction(self):
        print("State: Abgelenkt - Die Person ist unkonzentriert.")

    def handle_interaction(self):
        print("State: Interaktion - Der Bot spricht mit der Person.")

    def transition(self, event):
        if event in self.transitions[self.current_state]:
            new_state = self.transitions[self.current_state][event]
            print(f"Uebergang: {self.current_state} -> {new_state} durch Ereignis '{event}'")
            self.current_state = new_state
            
            # Gesichtsanzeige aktualisieren
            if self.current_state == "Fokussiert":
                self.face_display.create_face(True)
            elif self.current_state == "Abgelenkt":
                self.face_display.create_face(False)
        else:
            print(f"Ereignis '{event}' ist im Zustand '{self.current_state}' nicht erlaubt.")
