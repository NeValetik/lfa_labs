class FiniteAutomata:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def string_validation(self, input_string):
        current_states = {self.start_state}
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
            current_states = next_states
            if not current_states:
                return False
        return bool(current_states & self.final_states)