from time import sleep
from StateMaschine.state_machine import EducationStateMachine
from TTS_and_STT.AudioRecorder import AudioRecorder
from Commands.CommandValidator import CommandValidator
from Face_Display.pylips.speech import RobotFace
from Face_Display.pylips.face import FacePresets, ExpressionPresets

def main():
    # Initialisiere die State-Maschine, AudioRecorder und RobotFace
    education_bot_stateM = EducationStateMachine()
    audio_recorder = AudioRecorder()
    face = RobotFace()

    # Initialisiere CommandValidator
    command_validator = CommandValidator(education_bot_stateM, audio_recorder)

    # Setze das Gesicht in den Schlafmodus (Augen zu)
    face.set_appearance(FacePresets.default)
    face.express(ExpressionPresets.default_closed_eyes,100000000)  # Schlafmodus

    print(f"Initial State: {education_bot_stateM.current_state}")
    print("The bot is sleeping. Sage 'Start Bot' um Ihn aufzuwecken, drücke l um die Aufnahme zu starten.")

    try:
        while True:
            # Überprüfe den Zustand der State-Maschine
            if education_bot_stateM.current_state == "init":
                # Warten auf den "Start Bot"-Befehl
                print("Waiting for 'Start Bot' command...")
                command_validator.process_speech_command()

            elif education_bot_stateM.current_state == "startedBot":
                # Bot erwacht und begrüßt den Nutzer
                face.set_appearance(FacePresets.default)
                face.express(ExpressionPresets.happy)
                face.say("Hallo, ich bin dein Lehrassistenz. Wie kann ich dir helfen?")
                face.wait()
                print("Bot gestartet, Welcher Modus soll gestartet werden? Feies Lernen oder Fragerunde?")

            elif education_bot_stateM.current_state == "Q_and_A":
                # Bot wechselt zu Q&A-Modus
                face.set_appearance(FacePresets.default)
                face.express(ExpressionPresets.happy)
                face.say("Let's start with Q&A!")
                face.wait()
                # Hier kommt die Q&A-Logik rein mit llm, um die Fragen zu beantworten.

            elif education_bot_stateM.current_state == "free_learning":
                # Bot wechselt zu Free-Learning-Modus
                face.set_appearance(FacePresets.cutie)
                face.express(ExpressionPresets.happy)
                face.say("Let's start with Free Learning!")
                face.wait()
                # Hier kommt Attentionlogic rein. Wenn der Bot merkt, dass der Nutzer nicht mehr aktiv ist, soll er in den Attention-Modus wechseln.

            elif education_bot_stateM.current_state == "completed":
                # Bot beendet den Prozess
                face.set_appearance(FacePresets.default)
                face.express(ExpressionPresets.happy)
                face.say("Bye, see you next time!")
                face.wait()
                break  # Beende die Schleife

            sleep(0.5)  # CPU-Auslastung reduzieren

    except KeyboardInterrupt:
        print("Exiting...")
        audio_recorder.close()

if __name__ == "__main__":
    main()
