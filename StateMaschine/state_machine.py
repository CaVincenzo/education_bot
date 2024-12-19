from statemachine import StateMachine, State

class EducationStateMachine(StateMachine):

    # Alle States des EducationBots
    init = State('Init', initial=True)
    free_learning = State('Free-Learning')
    Q_and_A = State('Q&A')
    attention = State('Getting Attention')
    completed = State('Completed')

    # Transitions
    start_free_learning = init.to(free_learning)
    start_Q_and_A = init.to(Q_and_A)

    free_learning_to_Q_and_A = free_learning.to(Q_and_A)
    free_learning_to_attention = free_learning.to(attention)
    free_learning_to_completed = free_learning.to(completed)

    Q_and_A_to_free_learning = Q_and_A.to(free_learning)
    Q_and_A_to_attention = Q_and_A.to(attention)
    Q_and_A_to_completed = Q_and_A.to(completed)

    attention_to_free_learning = attention.to(free_learning)
    attention_to_Q_and_A = attention.to(Q_and_A)
    attention_to_completed = attention.to(completed)

    reset = completed.to(init)

    def __init__(self):
        super().__init__()

    # Define actions for each transition
    def on_start_free_learning(self):
        print("Transitioned from Init to Free Learning")
        # Add your logic here 

    def on_start_Q_and_A(self):
        print("Transitioned from Init to Q&A")
        # Add your logic here 

    def on_free_learning_to_Q_and_A(self):
        print("Transitioned from Free Learning to Q&A")
        # Add your logic here

    def on_free_learning_to_attention(self):
        print("Transitioned from Free Learning to Getting Attention")
        # Add your logic here

    def on_free_learning_to_completed(self):
        print("Transitioned from Free Learning to Completed")
        # Add your logic here

    def on_Q_and_A_to_free_learning(self):
        print("Transitioned from Q&A to Free Learning")
        # Add your logic here

    def on_Q_and_A_to_attention(self):
        print("Transitioned from Q&A to Getting Attention")
        # Add your logic here

    def on_Q_and_A_to_completed(self):
        print("Transitioned from Q&A to Completed")
        # Add your logic here

    def on_attention_to_free_learning(self):
        print("Transitioned from Getting Attention to Free Learning")
        # Add your logic here

    def on_attention_to_Q_and_A(self):
        print("Transitioned from Getting Attention to Q&A")
        # Add your logic here

    def on_attention_to_completed(self):
        print("Transitioned from Getting Attention to Completed")
        # Add your logic here

    def on_reset(self):
        print("Reset to Init")
        # Add your logic here

    # BeispielWorkflow der sodann in der main.py aufgerufen werden kann
    def beispielWorkflow(self):

         # Beispiel für einen Workflow: Init -> Free Learning -> Completed

        print("=== State Machine Test ===")
        print(f"Initial State: {self.current_state}")
        self.start_free_learning()
        print(f"Current State: {self.current_state}")
        self.free_learning_to_completed()
        print(f"Current State: {self.current_state}")
