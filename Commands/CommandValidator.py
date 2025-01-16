from StateMaschine.state_machine import EducationStateMachine
class CommandValidator:
    stateref = None
    def __init__(self, state_machine):
        """
        Initialisiert den CommandValidator mit Abhängigkeiten.
        :param state_machine: Die State-Maschine zur Steuerung.
        :param audio_recorder: Eine Instanz der AudioRecorder-Klasse zur Sprachaufnahme.
        """
        self.state_machine = state_machine


def validate_and_process(self, command: str):
    command = command.strip().lower()

    if command == "start bot":
        print("Command recognized: Start Bot")
        self.state_machine.start_bot()

    elif command == "start free learning":
        print("Command recognized: Start Free Learning")
        self.state_machine.start_free_learning()

    elif command == "start fragerunde":
        print("Command recognized: Start Fragerunde")
        self.state_machine.start_Q_and_A()

    elif command == "end bot":
        print("Command recognized: End Bot")
        self.state_machine.reset_bot()

    else:
        print(f"Unknown command: '{command}'")

