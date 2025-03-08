from lab1.FiniteAutomata import *
from lab2.Grammar2 import *
from collections import deque

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

  def NfaToDfa(self) -> FiniteAutomata:
    dfaStartState = self.startState
    dfaFinalStates  = [] 

    dfaStates = {}
    dfaTransitions = {}

    currentState = [self.startState]
    
    queue = deque([dfaStartState])

    while queue:
        currentState = queue.popleft()
        dfaTransitions[currentState] = {}

        for symbol in self.alphabet:
            newState = set()
            
            for nfaState in currentState:
                if (nfaState, symbol) in self.transitions:
                    newState.update(self.transitions[(nfaState, symbol)])

            if newState:
                if newState not in dfaStates:
                    dfaStates[newState] = newState
                    queue.append(newState)
                
                dfaTransitions[currentState][symbol] = newState

    for dfaState in dfaStates:
        if any(state in self.finalStates for state in dfaState):
            dfaFinalStates.add(dfaState)

    return FiniteAutomata(
        states=set(dfaStates.keys()),
        alphabet=self.alphabet,
        transitions=dfaTransitions,
        startState=dfaStartState,
        finalStates=dfaFinalStates
    )