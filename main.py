import os
from time import sleep
from StateMaschine.state_machine import EducationStateMachine
from TTS_and_STT.AudioRecorder import AudioRecorder
from Commands.CommandValidator import CommandValidator
from Face_Display.pylips.speech import RobotFace
from Face_Display.pylips.face import FacePresets, ExpressionPresets
import keyboard

def main():
    # Initialisiere die State-Maschine, AudioRecorder und RobotFace
    education_bot_stateM = EducationStateMachine()
    audio_recorder = AudioRecorder()
    face = RobotFace()  
    command_validator = CommandValidator(education_bot_stateM)

    
    # Setze das Gesicht in den Schlafmodus
    face.set_appearance(FacePresets.sleep)
    face.wait()
    print(f"Initial State: {education_bot_stateM.current_state}")
    print("The bot is sleeping. Sage 'Start Bot' um Ihn aufzuwecken, druecke l um die Aufnahme zu starten.")
    # face.say("Ich schlafe. Sage 'Start Bot' um mich aufzuwecken, druecke l um die Aufnahme zu starten.")
    face.wait()
    
    
    try:
        while True:
            # Überprüfe den Zustand der State-Maschine
            audio_path = "./recording.wav"
            
            if not os.path.exists(audio_path):
                print(f"Die Datei {audio_path} wurde nicht gefunden!")
            else:
                print(f"Die Datei {audio_path} existiert und ist zugänglich.")
            
            audioString = audio_recorder.transcribe_with_whisper(audio_path)
            print(audioString)
            command_validator.validate_and_process(audioString)
            
            # if keyboard.is_pressed("l"):
                
            #         audio = audio_recorder.start_audio_input()
            # if not os.path.exists(audio_path):
            #     print(f"Die Datei {audio_path} wurde nicht gefunden!")
            # else:
            #     print(f"Die Datei {audio_path} existiert und ist zugänglich.")
            #         print(audio)
            #         audioString = audio_recorder.transcribe_with_whisper("./"+audio)
            #         command_validator.validate_and_process(audioString)
                    
            if education_bot_stateM.current_state == education_bot_stateM.init:
                pass# Warten auf den "Start Bot"-Befehl

            elif education_bot_stateM.current_state == education_bot_stateM.startedBot:
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
