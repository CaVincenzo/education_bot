import os
from time import sleep
from StateMaschine.state_machine import EducationStateMachine
from TTS_and_STT.AudioRecorder import AudioRecorder
from Commands.CommandValidator import CommandValidator
from Face_Display.pylips.speech import RobotFace
from Face_Display.pylips.face import FacePresets, ExpressionPresets
import keyboard
from LLM.llm_query import MistralQuery

def main():
    # Initialisiere die State-Maschine, AudioRecorder und RobotFace
    education_bot_stateM = EducationStateMachine()
    audio_recorder = AudioRecorder()
    face = RobotFace()  
    command_validator = CommandValidator(education_bot_stateM)
    llmquery = MistralQuery()
    

    
    # Setze das Gesicht in den Schlafmodus
    face.set_appearance(FacePresets.sleep)
    face.wait()
    print(f"Initial State: {education_bot_stateM.current_state}")
    print("The bot is sleeping. Sage 'Start' um Ihn aufzuwecken, druecke l um die Aufnahme zu starten.")
    face.express(ExpressionPresets.sleep,100000000)
    face.wait()
    
    face.say("Ich schlafe. Sage 'Start' um mich aufzuwecken, drücke l um die Aufnahme zu starten.")
    face.wait()
    
    # Speichere den letzten verarbeiteten Zustand
    last_processed_state = None
    
    
    try:
        while True:
            # Überprüfe den Zustand der State-Maschine
            current_state = education_bot_stateM.current_state
            
            if keyboard.is_pressed("l"):
                
                    audio_path = audio_recorder.start_audio_input()
                    
                    if not os.path.exists(audio_path):
                        print(f"Die Datei {audio_path} wurde nicht gefunden!")
                    else:
                        print(f"Die Datei {audio_path} existiert und ist zugänglich.")
                        audioString = audio_recorder.transcribe_with_whisper("./" +audio_path)
                        print(f"Transkribierter Text: {audioString}")
                        command_validator.validate_and_process(audioString)
                    
            if current_state != last_processed_state:    
                if current_state == education_bot_stateM.init:
                    face.set_appearance(FacePresets.sleep)
                    face.express(ExpressionPresets.sleep, 100000000)
                    face.wait()
                    

                elif current_state == education_bot_stateM.startedBot:
                    # Bot erwacht und begrüßt den Nutzer
                    face.set_appearance(FacePresets.default)
                    face.express(ExpressionPresets.happy, 100000000)
                    face.say("Hallo, ich bin Mila dein Education Bot. Wie kann ich dir helfen? Welcher Modus soll gestartet werden? Feies Lernen oder Fragerunde?")
                    face.wait()
                    

                elif current_state == education_bot_stateM.Q_and_A:
                    # Bot wechselt zu Q&A-Modus
                    face.set_appearance(FacePresets.default)
                    face.express(ExpressionPresets.happy,1000000)
                    face.say("Let's start with Q&A!")
                    face.wait()
                    face.say("Was möchtest du wissen, drücke k um eine Frage zu stellen")
                    # inplementierung was passieren soll für Q&A
                    if keyboard.is_pressed('k'):
                        audio_path = audio_recorder.start_audio_input()
                        if not os.path.exists(audio_path):
                            print(f"Die Datei {audio_path} wurde nicht gefunden!")
                        else:
                            print(f"Die Datei {audio_path} existiert und ist zugänglich.")
                            audioString = audio_recorder.transcribe_with_whisper("./" +audio_path)
                            print(f"Transkribierter Text: {audioString}")
                            response = llmquery.query_Q_AND_A("","Was ist die Antwort auf die Frage: "+audioString, "","")
                            face.say(response)
                            face.wait()
                    

                elif current_state == education_bot_stateM.free_learning:
                    # Bot wechselt zu Free-Learning-Modus
                    face.set_appearance(FacePresets.cutie)
                    face.express(ExpressionPresets.happy)
                    face.say("Let's start with Free Learning!")
                    face.wait()
                    # Hier kommt Attentionlogic rein. Wenn der Bot merkt, dass der Nutzer nicht mehr aktiv ist, soll er in den Attention-Modus wechseln.

                elif current_state == education_bot_stateM.completed:
                    # Bot beendet den Prozess
                    face.set_appearance(FacePresets.default)
                    face.express(ExpressionPresets.sad)
                    face.say("Bye, see you next time!")
                    face.wait()
                    break  # Beende die Schleife
            
                # Aktualisiere den zuletzt verarbeiteten Zustand
                last_processed_state = current_state

            sleep(0.5)  # CPU-Auslastung reduzieren

    except KeyboardInterrupt:
        print("Exiting...")
        audio_recorder.close()

if __name__ == "__main__":
    main()
