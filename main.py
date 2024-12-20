from time import sleep
from StateMaschine.state_machine import EducationStateMachine

from Face_Display.PyLips.pylips.speech import RobotFace
from Face_Display.PyLips.pylips.face import FacePresets, ExpressionPresets
# https://github.com/interaction-lab/PyLips

def main_loop():
# Initialisiere die State-Maschine
    education_bot = EducationStateMachine()
    face = RobotFace()

    print("=== State Machine Test ===")
    print(f"Initial State: {education_bot.current_state}")
    face.set_appearance(FacePresets.default)
    face.say("Hello, welcome I am your EducationBot!")
    face.wait()
    # we should say start free learning
    
    education_bot.start_free_learning()
    print(f"Current State: {education_bot.current_state}")
    # change face with FacePresets
    face.set_appearance(FacePresets.cutie)
    face.set_appearance(ExpressionPresets.happy)
    face.say("Let's start with free learning.")
    face.wait()
    
    
    education_bot.on_free_learning_to_attention()
    print(f"Current State: {education_bot.current_state}")
    face.set_appearance(ExpressionPresets.angry)
    face.set_appearance(FacePresets.gingerbreadman)
    face.say("I am sad, Can you please Fokus on learning.")
    face.wait()
    
    
    education_bot.on_attention_to_completed()
    print(f"Current State: {education_bot.current_state}")
    face.set_appearance(FacePresets.default)
    face.set_appearance(ExpressionPresets.happy)
    face.say("Bye, see you next time!")
    face.wait()


if __name__ == "__main__":
    main_loop()