from lab1.FiniteAutomata import *
from lab2.Grammar2 import *

class FiniteAutomata2 (FiniteAutomata):
  def __init__(self, **args):
    super().__init__(**args)

  def finiteAutomatonToGrammar(self):
    Vn = self.alphabet
    Vt = self.states
    S = self.startState
    P = {}

    for key, values in self.transitions.items():
      for value in values:
        if key[0] not in P.keys():
          P[key[0]] = [key[1] + value]
        else:
          if key[0] in self.finalStates:
            P[key[0]].append(key[1])
          P[key[0]].append(key[1] + value)

    return Grammar2(
      Vn = Vn,
      Vt = Vt,
      S = S,
      P = P,
    )
  
  def isDetermenistic(self):
    for state in self.states:
      for symbol in self.alphabet:
        if isinstance(state, frozenset):
          if (state, symbol) not in self.transitions:
            continue  # Missing transitions are allowed
          if len(self.transitions[(state, symbol)]) != 1:
            return False
        else:
          if (state, symbol) not in self.transitions:
            continue  # Missing transitions are allowed
          if len(self.transitions[(state, symbol)]) > 1:
            return False
    return True

  def NfaToDfa(self):
    dfaStates = set()
    dfaTransitions = {}
    dfaFinalStates = set()
    
    # Start with the start state
    startStateSet = frozenset([self.startState])
    unmarkedStates = [startStateSet]
    dfaStates.add(startStateSet)
    
    # Process all unmarked state sets
    while unmarkedStates:
      currentStateSet = unmarkedStates.pop(0)
      
      # Check if this is a final state
      if any(state in self.finalStates for state in currentStateSet):
        dfaFinalStates.add(currentStateSet)
      
      # For each symbol in the alphabet
      for symbol in self.alphabet:
        nextStateSet = frozenset(
          nextState
          for state in currentStateSet
          for nextState in self.transitions.get((state, symbol), set())
        )
        
        if not nextStateSet:
          continue  # No transition for this symbol
        
        # Add the transition
        dfaTransitions[(currentStateSet, symbol)] = {nextStateSet}
        
        # If this is a new state, add it to be processed
        if nextStateSet not in dfaStates:
          dfaStates.add(nextStateSet)
          unmarkedStates.append(nextStateSet)
    return FiniteAutomata(
      dfaStates,
      self.alphabet,
      dfaTransitions,
      startStateSet,
      dfaFinalStates
    )
    
  # def NfaToDfa(self):
  #   grammar = {}
    
  #   return grammar
