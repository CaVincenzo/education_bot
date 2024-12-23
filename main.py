import asyncio
from time import sleep
from StateMaschine.state_machine import EducationStateMachine

from LLM.llm_query import MistralQuery
from Face_Display.PyLips.pylips.speech import RobotFace
from Face_Display.PyLips.pylips.face import FacePresets, ExpressionPresets
# https://github.com/interaction-lab/PyLips

def main_loop():
# Initialisiere die State-Maschine
    education_bot_stateM = EducationStateMachine()
    # face = RobotFace()
    llm_query = MistralQuery()

    # Parameter definieren
    context = "Du bist ein Lehrassistenz-System für Medieninformatiker aus dem 6. Semester.\n"
    prompt = "Hallo bist du Online"
    input_file_path = "LLM\Input.txt"
    FL_output_file_path = "LLM\OutputFreeLearning.txt"
    Q_and_A_output_file_path = "LLM\OutputQandA.txt"
    # Rufe die Methode auf
    FL_response = asyncio.run(llm_query.query_FreeLearning(context, prompt, FL_output_file_path))
    print("Antwort des FL_LLMs:", FL_response)
    # Ausgabe der Antwort
   
    # print("=== State Machine Test ===")
    # print(f"Initial State: {education_bot_stateM.current_state}")
    # face.set_appearance(FacePresets.default)
    # face.say(responsetext)
    # face.express(ExpressionPresets.angry, 2)
    # face.wait()


    # we should say start free learning
    
    # education_bot_stateM.start_free_learning()
    # print(f"Current State: {education_bot_stateM.current_state}")
    # # change face with FacePresets
    # face.set_appearance(FacePresets.cutie)
    # face.express(ExpressionPresets.happy)
    # face.say("Let's start with free learning.")
    # face.wait()
    
    
    # education_bot_stateM.on_free_learning_to_attention()
    # print(f"Current State: {education_bot_stateM.current_state}")
    # face.express(ExpressionPresets.angry)
    # face.set_appearance(FacePresets.gingerbreadman)
    # face.say("I am sad, Can you please Fokus on learning.")
    # face.wait()
    
    
    # education_bot_stateM.on_attention_to_completed()
    # print(f"Current State: {education_bot_stateM.current_state}")
    # face.set_appearance(FacePresets.default)
    # face.express(ExpressionPresets.happy)
    # face.say("Bye, see you next time!")
    # face.wait()


if __name__ == "__main__":
    main_loop()