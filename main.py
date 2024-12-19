from time import sleep
from StateMaschine.state_machine import EducationStateMachine

from Face_Display.PyLips.pylips.speech import RobotFace
# https://github.com/interaction-lab/PyLips

def main_loop():
# Initialisiere die State-Maschine
    education_bot = EducationStateMachine()
    face = RobotFace()

    education_bot.beispielWorkflow()
    
    # you may need to wait here for a minute or two to let allosaurus download on the first run

    face.say("Hello, welcome to pylips!")
    sleep(5)
    face.say("Hallo Mika, ich bin dein neuer Roboterfreund. Ich werde dir heute einiges beibringen.")


if __name__ == "__main__":
    main_loop()