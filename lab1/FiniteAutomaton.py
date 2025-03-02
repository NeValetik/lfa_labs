class FiniteAutomata:
  def __init__(self, **args):
    self.states = args.get("states")
    self.alphabet = args.get("alphabet")
    self.transitions = args.get("transitions")
    self.startState = args.get("startState")
    self.finalStates = args.get("finalStates")

  def stringValidation(self, inp):
    stateTrack = [self.startState] 

    for ch in inp:
      if ch not in self.alphabet:
        return False
      
      nextStates = []
      for state in stateTrack:
        if (state, ch) in self.transitions:
          nextStates = self.transitions[(state, ch)] 
      
      if not nextStates:
        return False
      
      stateTrack = nextStates 

    return any(state in self.finalStates for state in stateTrack)