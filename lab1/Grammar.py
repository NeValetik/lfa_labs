from lab1.FiniteAutomata import * 
import random
class Grammar:

  def __init__(self, **args):
    self.Vn = args.get("Vn")
    self.Vt = args.get("Vt")
    self.P = args.get("P")
    self.S = args.get("S")

  def generateValidString(self):
    current = self.S        
    while any(symbol in self.Vn for symbol in current):
      string = ""
      for symbol in current:
        if symbol in self.Vn:
          string += random.choice(self.P[symbol])
        else:
          string += symbol
      current = string
    return current

  def toFiniteAutomata(self):
    states = set(self.Vn)
    alphabet = set(self.Vt)
    startState = self.S
    finalStates = [""]
    transitionFunction = {}

    for nonTerm, res in self.P.items():
      for sequence in res:
        statePos = next((i for i, c in enumerate(sequence) if c in states), -1) # should be also updated to more non-terminals

        key = (
          nonTerm, 
          sequence[:statePos] if statePos != -1 else sequence
        )

        value = sequence[statePos] if statePos != -1 else ""

        if key not in transitionFunction:
          transitionFunction[key] = [value]
        elif value not in transitionFunction[key]:  
          transitionFunction[key].append(value)

    return FiniteAutomata( 
      states = states, 
      alphabet = alphabet, 
      startState = startState, 
      finalStates = finalStates, 
      transitions = transitionFunction
    )    