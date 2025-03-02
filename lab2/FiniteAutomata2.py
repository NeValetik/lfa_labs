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
          P[key[0]].append(key[1] + value)
        if key[0] in self.finalStates:
          P[key[0]].append(key[1])

    return Grammar2(
      Vn = Vn,
      Vt = Vt,
      S = S,
      P = P,
    )

    
  # def NfaToDfa(self):
  #   grammar = {}
    
  #   return grammar
