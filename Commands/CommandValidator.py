from StateMaschine.state_machine import EducationStateMachine
from rapidfuzz import fuzz, process

class CommandValidator:
    def __init__(self, state_machine,face):
        """
        Initialisiert den CommandValidator mit Abhängigkeiten.
        :param state_machine: Die State-Maschine zur Steuerung.
        """
        self.state_machine = state_machine
        self.face = face
        self.commands = {
            "start": {
                "action": self.state_machine.start_bot,
                "synonyms": ["begin", "start bot", "activate bot"]
            },
            "free learning": {
                "action": self.state_machine.start_free_learning,
                "synonyms": ["learning mode", "starte freies lernen", "study mode", "freies Lernen", "start free learning"]
            },
            "fragerunde": {
                "action": self.state_machine.start_Q_and_A,
                "synonyms": ["q and a", "questions", "start fragerunde", "fragerunde", "start q&a"]
            },
            "end bot": {
                "action": self.state_machine.transition_to_completed,
                "synonyms": ["terminate", "stop bot", "end","end bot","fertig mit lernen","beenden"]
            }
        }

    def validate_and_process(self, command: str):
        command = command.strip().lower()

        # Flache Liste aller möglichen Eingaben erstellen
        flat_commands = {
            synonym: key
            for key, details in self.commands.items()
            for synonym in [key] + details["synonyms"]
        }

        # Fuzzy-Matching mit erlaubten Befehlen
        match, score, _ = process.extractOne(command, flat_commands.keys(), scorer=fuzz.ratio)

        # Schwellenwert für die Erkennung (z. B. 80%)
        if score >= 75:
            recognized_command = flat_commands[match]
            print(f"Command recognized: {recognized_command} (Score: {score})")
            self.commands[recognized_command]["action"]()  # Führe die zugehörige Aktion aus
        else:
            print(f"Unknown command: '{command}' (Best match: {match}, Score: {score})")
            self.face.say("Ich habe dich nicht verstanden. Bitte wiederhole deinen Befehl.")
            
