class CommandValidator:
    def __init__(self, state_machine, audio_recorder):
        """
        Initialisiert den CommandValidator mit Abhängigkeiten.
        :param state_machine: Die State-Maschine zur Steuerung.
        :param audio_recorder: Eine Instanz der AudioRecorder-Klasse zur Sprachaufnahme.
        """
        self.state_machine = state_machine
        self.audio_recorder = audio_recorder

    def process_speech_command(self):
        """
        Nimmt einen Sprachbefehl auf, transkribiert ihn und verarbeitet ihn.
        """
        print("Recording your command. Hold the key and speak.")
        audio_file_path = self.audio_recorder.start_audio_input("command.wav")

        # Transkribiere den Sprachbefehl mit Whisper
        recognized_command = self.audio_recorder.transcribe_with_whisper(audio_file_path)

        if recognized_command:
            print(f"Recognized command: {recognized_command}")
            self.validate_and_process(recognized_command)
        else:
            print("Could not recognize any command.")

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

