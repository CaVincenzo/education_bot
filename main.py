import os
from time import sleep
from StateMaschine.state_machine import EducationStateMachine
from TTS_and_STT.AudioRecorder import AudioRecorder
from Commands.CommandValidator import CommandValidator
from pylips.speech import RobotFace
from pylips.face import FacePresets, ExpressionPresets
import keyboard
import subprocess
from LLM.llm_query import MistralQuery


def main():
    # Initialisiere die State-Maschine, AudioRecorder und RobotFace
    education_bot_stateM = EducationStateMachine()
    audio_recorder = AudioRecorder()
    face = RobotFace()  
    command_validator = CommandValidator(education_bot_stateM,face)
    llmquery = MistralQuery()
    
    # Testen der LLM-Abfrage
    # context = "Du bist ein Lehrassistenz-System für Medieninformatiker aus dem 7. Semester.\n"
    # Q_and_A_output_file_path = "LLM\OutputQandA.txt"
    # Foliensatz_file_path = "LLM\Foliensatz.txt"
    # response = llmquery.query_Q_AND_A(context,"Testfrage Bist du Online",Foliensatz_file_path, Q_and_A_output_file_path)
    # print("Response from llm" + response)
    
    # Setze das Gesicht in den Schlafmodus
   
    print(f"Initial State: {education_bot_stateM.current_state}")
    print(" Sage 'Start' um Ihn aufzuwecken, druecke l um die Aufnahme zu starten.")
    face.set_appearance(FacePresets.default)
    face.express(ExpressionPresets.happy, 10000)
    face.wait() 
    face.say(" Sage 'Start' oder 'Begin' um Mila zu starten, für die Aufnahme drücke l gedrückt")
    face.wait()
    
    # Speichere den letzten verarbeiteten Zustand
    last_processed_state = None
    # Variable für den Subprozess
    attentionProcess = None
    
    try:
        while True:
            # Überprüfe den Zustand der State-Maschine
            pressed_key = audio_recorder.get_pressed_key()
            current_state = education_bot_stateM.current_state
            
            # Zustand "free_learning" (Subprozess starten)
            if current_state == education_bot_stateM.free_learning:
                if attentionProcess is None or attentionProcess.poll() is not None:
                    print("Starte Subprozess für Aufmerksamkeitserkennung...")
                    attentionProcess = subprocess.Popen(["python", "HeadPoseEstimation/distractionDetection.py"])
            
            # Zustandswechsel (Subprozess beenden)
            elif current_state != education_bot_stateM.free_learning:
                if attentionProcess is not None:
                    print("Beende Subprozess für Aufmerksamkeitserkennung...")
                    attentionProcess.terminate()
                    attentionProcess.wait()  # Warte, bis der Subprozess beendet ist
                    attentionProcess = None
            
            # Audioaufnahme starten
            if pressed_key == 'l':

                    audio_path = audio_recorder.start_audio_input()
                    
                    if audio_path is None:
                        print("Keine Aufnahme erfolgt. Bitte versuchen Sie es erneut.")
                    else:
                        print(f"Die Datei {audio_path} wurde erfolgreich aufgenommen.")
                        audioString = audio_recorder.transcribe_with_whisper("./" +audio_path)
                        print(f"Transkribierter Text: {audioString.encode('ascii',errors='replace')}")
                        command_validator.validate_and_process(audioString)
                        
            #Logic um ein Prompt zu erstellen und eine Frage zu stellen
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
                        
                        response = llmquery.query_Q_AND_A(context,"Was ist die Antwort auf die Frage: "+prompt,Foliensatz_file_path, Q_and_A_output_file_path)
                        # print(f"Response from llm{response}" )
                        
                        face.say(response)
                        face.wait()
                        
                        face.say("Möchtest du noch eine Frage stellen?, dann drücke k für das starten der Aufnahme gedrückt")
                        face.wait()
                        
            # Überprüfe, ob sich der Zustand geändert hat, damit der selbe Zustand nicht mehrmals verarbeitet wird
            if current_state != last_processed_state:    
                
                if current_state == education_bot_stateM.init:
                    
                    face.express(ExpressionPresets.happy, 100000000)
                    face.wait()
                    

                elif current_state == education_bot_stateM.startedBot:
                    print(f" current state: {current_state}")
                    # Bot erwacht und begrüßt den Nutzer
                    face.set_appearance(FacePresets.default)
                    face.express(ExpressionPresets.happy, 100000000)
                    face.wait()
                    face.say("Hallo, ich bin Mila dein Education Bot. Wie kann ich dir helfen? Welcher Modus soll gestartet werden? Feies Lernen oder Fragerunde?")
                    face.wait()
                    #logic für winken

                elif current_state == education_bot_stateM.Q_and_A:
                    print(f" current state: {current_state}")
                    # Bot wechselt zu Q&A-Modus
                    face.express(ExpressionPresets.happy,1000000)
                    face.wait()
                    face.say("Lass uns mit der Fragerunde starten, Was möchtest du wissen, drücke k um eine Frage zu stellen")
                    face.wait()
                    
                elif current_state == education_bot_stateM.completed:
                    print(f" current state: {current_state}")
                    # Bot beendet den Prozess
                    face.say("Bye, see you next time!")
                    face.wait()
                    #logic für winken
                    break  # Beende die Schleife
            
                # Aktualisiere den zuletzt verarbeiteten Zustand
                last_processed_state = current_state

            sleep(0.5)  # CPU-Auslastung reduzieren

    except KeyboardInterrupt:
        print("Exiting...")
        audio_recorder.close()

if __name__ == "__main__":
    main()
