from StateMaschine.state_machine import EducationStateMachine

def main_loop():
# Initialisiere die State-Maschine
    education_bot = EducationStateMachine()

    education_bot.beispielWorkflow()
    
   

if __name__ == "__main__":
    main_loop()