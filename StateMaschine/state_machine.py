from statemachine import StateMachine, State

class EducationStateMachine(StateMachine):

    # Alle States des EducationBots
    init = State('Init', initial=True)
    startedBot = State('Started Bot')
    free_learning = State('Free-Learning')
    Q_and_A = State('Fragerunde')
    attention = State('Getting Attention')
    completed = State('Completed')

    # Transitions
    init_to_startedBot = init.to(startedBot)

    startedBot_to_free_learning = startedBot.to(free_learning)
    startedBot_to_Q_and_A = startedBot.to(Q_and_A)

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

    # Define actions for transitions
    def start_bot(self):
        """
        Trigger transition from Init to Started Bot.
        """
        if self.current_state == self.init:
            self.init_to_startedBot()
            print("Bot started. Transitioned to 'Started Bot' state.")

    def start_free_learning(self):
        """
        Trigger transition from Started Bot to Free Learning.
        """
        if self.current_state == self.startedBot:
            self.startedBot_to_free_learning()
            print("Transitioned to 'Free Learning' state.")

    def start_Q_and_A(self):
        """
        Trigger transition from Started Bot to Q&A.
        """
        if self.current_state == self.startedBot:
            self.startedBot_to_Q_and_A()
            print("Transitioned to 'Q&A' state.")

    def transition_to_attention(self):
        """
        Transition from Free Learning or Q&A to Attention.
        """
        if self.current_state == self.free_learning:
            self.free_learning_to_attention()
            print("Transitioned to 'Getting Attention' state.")
        elif self.current_state == self.Q_and_A:
            self.Q_and_A_to_attention()
            print("Transitioned to 'Getting Attention' state.")

    def transition_to_completed(self):
        """
        Transition from any state to Completed.
        """
        if self.current_state == self.free_learning:
            self.free_learning_to_completed()
        elif self.current_state == self.Q_and_A:
            self.Q_and_A_to_completed()
        elif self.current_state == self.attention:
            self.attention_to_completed()
        print("Transitioned to 'Completed' state.")

    def reset_bot(self):
        """
        Reset to the initial state.
        """
        if self.current_state == self.completed:
            self.reset()
            print("Bot reset to 'Init' state.")

    # Transition hooks
    def on_init_to_startedBot(self):
        print("Transitioned from Init to Started Bot.")

    def on_startedBot_to_free_learning(self):
        print("Transitioned from Started Bot to Free Learning.")

    def on_startedBot_to_Q_and_A(self):
        print("Transitioned from Started Bot to Q&A.")

    def on_free_learning_to_attention(self):
        print("Transitioned from Free Learning to Getting Attention.")

    def on_free_learning_to_completed(self):
        print("Transitioned from Free Learning to Completed.")

    def on_Q_and_A_to_attention(self):
        print("Transitioned from Q&A to Getting Attention.")

    def on_Q_and_A_to_completed(self):
        print("Transitioned from Q&A to Completed.")

    def on_reset(self):
        print("Reset to Init.")
