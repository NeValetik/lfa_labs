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
        if value in self.finalStates:
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


  def _stringToStateSet(self, state_string):
    """Convert a string representation back to a set of states"""
    if state_string == "DFA_EMPTY":
      return set()
    return set(state_string[4:].split("_"))  # Remove "DFA_" prefix and split

  def NfaToDfa(self):
    # Dictionary to store epsilon closures for each state
    epsilonClosure = {}
    for state in self.states:
      epsilonClosure[state] = self.getEpsilonClosure(state)
    
    # First state of DFA will be epsilon closure of start state of NFA
    startStateSet = epsilonClosure[self.startState]
    startStateStr = self._stateSetToString(startStateSet)
    
    # Lists to track states to process and already processed states
    dfaStack = [startStateSet]
    dfaStates = [startStateSet]
    dfaStatesStr = {startStateStr}
    
    # Create output components for DFA
    dfaTransitions = {}
    dfaFinalStates = set()
    
    # Check if start state is final
    if any(state in self.finalStates for state in startStateSet):
      dfaFinalStates.add(startStateStr)
    
    # Process all states in the stack
    while dfaStack:
      currentStateSet = dfaStack.pop(0)
      currentStateStr = self._stateSetToString(currentStateSet)
      
      # Process each alphabet symbol (excluding epsilon if present)
      for symbol in self.alphabet:
        # Skip epsilon transitions in the main loop as they're handled via epsilon closure
        if symbol == 'e':
          continue
            
        # Compute the next state set for this symbol
        nextStateSet = set()
        
        # For each state in current set, find transitions and apply epsilon closure
        for state in currentStateSet:
          if (state, symbol) in self.transitions:
              # Get direct transitions
            direct_states = self.transitions[(state, symbol)]
            
            # For each direct state, add its epsilon closure
            for direct_state in direct_states:
              if direct_state in epsilonClosure:
                nextStateSet.update(epsilonClosure[direct_state])
              else:
                nextStateSet.add(direct_state)
        
          # Convert to string representation
          nextStateStr = self._stateSetToString(nextStateSet)
          
          # Add transition
          dfaTransitions[(currentStateStr, symbol)] = {nextStateStr}
          
          # If this is a new state, add it to be processed
          if nextStateStr not in dfaStatesStr and nextStateSet:
            dfaStack.append(nextStateSet)
            dfaStates.append(nextStateSet)
            dfaStatesStr.add(nextStateStr)
              
              # Check if it's a final state
            if any(state in self.finalStates for state in nextStateSet):
              dfaFinalStates.add(nextStateStr)
          
          # Handle empty set case (dead state)
          if not nextStateSet:
            deadState = self._stateSetToString(set())
            dfaTransitions[(currentStateStr, symbol)] = {deadState}
            
            # Add dead state if not already present
            if deadState not in dfaStatesStr:
              dfaStatesStr.add(deadState)
              
              # Add transitions from dead state to itself for all symbols
              for alpha in self.alphabet:
                if alpha != 'e':  # Skip epsilon
                  dfaTransitions[(deadState, alpha)] = {deadState}
    
    # Convert state sets to string representation for the final DFA
    dfaStatesFinal = dfaStatesStr
    
    # Create and return the DFA
    return FiniteAutomata2(
      states = dfaStatesFinal,
      alphabet = [a for a in self.alphabet if a != 'e'],  # Exclude epsilon
      transitions = dfaTransitions,
      startState = startStateStr,
      finalStates = dfaFinalStates
    )

  def getEpsilonClosure(self, state):
    """
    Compute the epsilon closure of a state (all states reachable via epsilon transitions)
    """
    closure = set([state])
    stack = [state]
    
    while stack:
      current = stack.pop(0)
      
      # If there are epsilon transitions from current state
      if (current, 'e') in self.transitions:
        for nextState in self.transitions[(current, 'e')]:
          if nextState not in closure:
            closure.add(nextState)
            stack.append(nextState)
    
    return closure

  def _stateSetToString(self, nextState):
    """Convert a set of states to a string representation"""
    if not nextState:
      return "DFA_EMPTY"
    sortedStates = sorted(list(nextState))
    return "DFA_" + "_".join(str(state) for state in sortedStates)