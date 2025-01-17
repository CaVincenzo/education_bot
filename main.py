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
            pressed_key = audio_recorder.get_pressed_key()
            current_state = education_bot_stateM.Q_and_A

            
            if pressed_key == 'l':

                    audio_path = audio_recorder.start_audio_input()
                    
                    if audio_path is None:
                        print("Keine Aufnahme erfolgt. Bitte versuchen Sie es erneut.")
                    else:
                        print(f"Die Datei {audio_path} wurde erfolgreich aufgenommen.")
                        audioString = audio_recorder.transcribe_with_whisper("./" +audio_path)
                        print(f"Transkribierter Text: {audioString}")
                        command_validator.validate_and_process(audioString)
            
            elif pressed_key == 'k':
                # erstellung von Prompts
                    audio_path = audio_recorder.start_audio_input()
                    
                    if not os.path.exists(audio_path):
                        print(f"Die Datei {audio_path} wurde nicht gefunden!")
                    else:
                        prompt = audio_recorder.transcribe_with_whisper("./" +audio_path)
                        context = "Du bist ein Lehrassistenz-System für Medieninformatiker aus dem 7. Semester.\n"
                        Q_and_A_output_file_path = "LLM\OutputQandA.txt"
                        Foliensatz_file_path = "LLM\Foliensatz.txt"
                        print(f"Transkribierter Text: {prompt}")
                        
                        llmquery.query_Q_AND_A(context,"Was ist die Antwort auf die Frage: "+prompt,Foliensatz_file_path, Q_and_A_output_file_path)
                        face.say(Q_and_A_output_file_path)
                        
                    
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
                    face.say("Lass uns mit der Fragerunde starten, Was möchtest du wissen, drücke k um eine Frage zu stellen")
                    face.wait()
                    
                    # inplementierung was passieren soll für Q&A geht noch nicht
                    
                    

                elif current_state == education_bot_stateM.free_learning:
                    # Bot wechselt zu Free-Learning-Modus
                    face.set_appearance(FacePresets.default)
                    face.express(ExpressionPresets.happy,10000)
                    face.say("Let's start with Free Learning!")
                    face.wait()
                    # Hier kommt Attentionlogic rein. Wenn der Bot merkt, dass der Nutzer nicht mehr aktiv ist, soll er in den Attention-Modus wechseln.

                elif current_state == education_bot_stateM.completed:
                    # Bot beendet den Prozess
                    face.set_appearance(FacePresets.default)
                    face.express(ExpressionPresets.sad,1000)
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
