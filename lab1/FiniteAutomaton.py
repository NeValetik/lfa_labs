class FiniteAutomata:
    def __init__(self, **args):
      self.states = args.get("states")
      self.alphabet = args.get("alphabet")
      self.transitions = args.get("transitions")
      self.startState = args.get("startState")
      self.finalStates = args.get("finalStates")

    def stringValidation(self, inp):
      stateTrack = self.startState

      for ch in inp:
        if ch not in self.alphabet:
          return False
        
        if (stateTrack, ch) not in self.transitions:
          return False
        
        stateTrack = self.transitions[(stateTrack, ch)][0] # logic should be added for scalability

      return stateTrack in self.finalStates            